from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import json
import re
import pandas as pd
from datetime import datetime
from utils.email_extractor import extract_emails_from_text, extract_emails_from_html
from utils.url_extractor import extract_urls_from_text, extract_urls_from_html
from utils.web_scraper import scrape_website, scrape_paginated_website
import io
import uuid
import glob
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli-anahtar-buraya'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
TEMP_FOLDER = 'temp_results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

def save_temp_results(data):
    for f in glob.glob(os.path.join(TEMP_FOLDER, '*.json')):
        if time.time() - os.path.getmtime(f) > 3600:
            try:
                os.remove(f)
            except Exception:
                pass
    key = str(uuid.uuid4())
    path = os.path.join(TEMP_FOLDER, f"{key}.json")
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False)
    return key

def load_temp_results(key):
    if not key:
        return {}
    path = os.path.join(TEMP_FOLDER, f"{key}.json")
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)

ALLOWED_EXTENSIONS = {'txt', 'html', 'htm', 'csv', 'json', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/url-to-email')
def url_to_email_page():
    return render_template('url_to_email_converter.html')

@app.route('/excel-email-merger')
def excel_email_merger_page():
    return render_template('excel_email_merger.html')

@app.route('/paginated-scan')
def paginated_scan_page():
    return render_template('paginated_scan.html')

@app.route('/extract', methods=['POST'])
def extract():
    results = {
        'emails': [],
        'urls': [],
        'source': '',
        'files': [],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if 'url_input' in request.form and request.form['url_input']:
        url = request.form['url_input']
        results['source'] = 'url'
        results['files'] = [url]
        
        try:
            deep_scan = 'deep_scan' in request.form
            max_pages = 5 if deep_scan else 1
            html_content, emails, urls = scrape_website(url, max_pages=max_pages)
            results['emails'] = emails
            results['urls'] = urls
        except Exception as e:
            return render_template('results.html', error=str(e))
    
    elif 'files' in request.files:
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return "Dosya seçilmedi", 400
        
        file_list = []
        all_emails = set()
        all_urls = set()
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                file_list.append(filename)
                
                file_ext = filename.rsplit('.', 1)[1].lower()
                
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if file_ext in ['html', 'htm']:
                    all_emails.update(extract_emails_from_html(content))
                    all_urls.update(extract_urls_from_html(content))
                else:
                    all_emails.update(extract_emails_from_text(content))
                    all_urls.update(extract_urls_from_text(content))
        
        results['source'] = 'files'
        results['files'] = file_list
        results['emails'] = sorted(all_emails)
        results['urls'] = sorted(all_urls)
    
    results['result_key'] = save_temp_results(results)
    return render_template('results.html', results=results)

@app.route('/scan-paginated', methods=['POST'])
def scan_paginated():
    base_url = request.form.get('base_url', '')
    start_page = int(request.form.get('start_page', 1))
    end_page = int(request.form.get('end_page', 1))
    delay = float(request.form.get('delay', 1))
    
    if not base_url:
        return render_template('paginated_scan.html', error="Lütfen bir URL girin!")
    
    try:
        all_emails, all_urls, scraped_pages = scrape_paginated_website(
            base_url, start_page, end_page, delay
        )
        
        results = {
            'base_url': base_url,
            'start_page': start_page,
            'end_page': end_page,
            'scraped_pages': scraped_pages,
            'emails': sorted(all_emails),
            'urls': sorted(all_urls),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        results['result_key'] = save_temp_results(results)
        return render_template('paginated_scan.html', results=results)
        
    except Exception as e:
        return render_template('paginated_scan.html', error=str(e))

@app.route('/convert-urls', methods=['POST'])
def convert_urls():
    if 'files' not in request.files:
        return render_template('url_to_email_converter.html', error="Dosya seçilmedi")
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return render_template('url_to_email_converter.html', error="Dosya seçilmedi")
    
    all_content = []
    file_list = []
    
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            file_list.append(filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    all_content.append(f.read())
            except Exception as e:
                print(f"Dosya okuma hatası {filename}: {e}")
    
    content = '\n'.join(all_content)
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s<>"{}|\\^`\[\]]*|www\.[^\s<>"{}|\\^`\[\]]+'
    
    found_emails = list(set(re.findall(email_pattern, content)))
    found_urls = list(set(re.findall(url_pattern, content)))
    
    conversions = []
    converted_emails = []
    stats = {'priority1': 0, 'priority2': 0, 'priority3': 0, 'priority4': 0, 'priority5': 0, 'other': 0}
    
    for url in found_urls:
        priority = 0
        converted = None
        domain = None
        
        if url.startswith('https://www.'):
            domain = url.replace('https://www.', '').split('/')[0].split('?')[0]
            converted = f"info@{domain}"
            priority = 1
            stats['priority1'] += 1
        elif url.startswith('http://www.'):
            domain = url.replace('http://www.', '').split('/')[0].split('?')[0]
            converted = f"info@{domain}"
            priority = 2
            stats['priority2'] += 1
        elif url.startswith('https://') and not url.startswith('https://www.'):
            domain = url.replace('https://', '').split('/')[0].split('?')[0]
            converted = f"info@{domain}"
            priority = 3
            stats['priority3'] += 1
        elif url.startswith('http://') and not url.startswith('http://www.'):
            domain = url.replace('http://', '').split('/')[0].split('?')[0]
            converted = f"info@{domain}"
            priority = 4
            stats['priority4'] += 1
        elif url.startswith('www.'):
            domain = url.replace('www.', '').split('/')[0].split('?')[0]
            converted = f"info@{domain}"
            priority = 5
            stats['priority5'] += 1
        else:
            stats['other'] += 1
        
        if converted:
            conversions.append({
                'original': url,
                'converted': converted,
                'priority': priority,
                'domain': domain
            })
            converted_emails.append(converted)
    
    results = {
        'emails': found_emails,
        'found_urls': len(found_urls),
        'converted_emails': sorted(list(set(converted_emails))),
        'conversions': sorted(conversions, key=lambda x: x['priority']),
        'stats': stats,
        'files': file_list,
        'file_count': len(file_list),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    results['result_key'] = save_temp_results(results)
    return render_template('url_to_email_converter.html', results=results)

@app.route('/merge-excel-emails', methods=['POST'])
def merge_excel_emails():
    if 'files' not in request.files:
        return "Dosya seçilmedi", 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return "Dosya seçilmedi", 400
    
    include_domains = 'include_domains' in request.form
    all_emails = set()
    file_list = []
    total_cells = 0
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            file_list.append(filename)
            
            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
                else:
                    df = pd.read_excel(filepath)
                
                for column in df.columns:
                    for value in df[column].dropna():
                        total_cells += 1
                        found_emails = re.findall(email_pattern, str(value))
                        for email in found_emails:
                            all_emails.add(email.lower())
            except Exception as e:
                print(f"Hata {filename}: {e}")
    
    unique_emails = sorted(list(all_emails))
    domains = sorted({email.split('@')[1] for email in unique_emails})
    domain_stats = {}
    for email in unique_emails:
        domain = email.split('@')[1]
        domain_stats[domain] = domain_stats.get(domain, 0) + 1
    
    results = {
        'files': file_list,
        'file_count': len(file_list),
        'total_cells': total_cells,
        'unique_emails': unique_emails,
        'domains': domains,
        'domain_stats': domain_stats if include_domains else None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    results['result_key'] = save_temp_results(results)
    return render_template('excel_email_merger.html', results=results)

@app.route('/download', methods=['POST'])
def download():
    key = request.form.get('result_key', '')
    file_type = request.form.get('type', 'txt')
    data = load_temp_results(key)
    emails = data.get('emails', [])
    urls = data.get('urls', [])
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')

    if file_type == 'emails':
        content = '\n'.join(emails)
        return create_download_response(content, f"emails_{ts}.txt")
    elif file_type == 'urls':
        content = '\n'.join(urls)
        return create_download_response(content, f"urls_{ts}.txt")
    elif file_type == 'csv':
        max_len = max(len(emails), len(urls)) if (emails or urls) else 0
        df = pd.DataFrame({
            'Email': emails + [''] * (max_len - len(emails)),
            'URL':   urls   + [''] * (max_len - len(urls))
        })
        output = io.BytesIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"results_{ts}.csv", mimetype='text/csv')
    elif file_type == 'json':
        result = {'emails': emails, 'urls': urls, 'timestamp': datetime.now().isoformat()}
        return create_download_response(json.dumps(result, indent=2, ensure_ascii=False), f"results_{ts}.json")
    return "Geçersiz dosya tipi", 400

@app.route('/download-converted', methods=['POST'])
def download_converted():
    key = request.form.get('result_key', '')
    file_type = request.form.get('type', 'txt')
    data = load_temp_results(key)
    # url_to_email sayfası -> converted_emails, excel_merger -> unique_emails
    emails = data.get('converted_emails', data.get('unique_emails', []))
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')

    if file_type == 'txt':
        return create_download_response('\n'.join(emails), f"emails_{ts}.txt")
    elif file_type == 'csv':
        output = io.BytesIO()
        pd.DataFrame({'Email': emails}).to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"emails_{ts}.csv", mimetype='text/csv')
    elif file_type == 'excel':
        output = io.BytesIO()
        pd.DataFrame({'Email': emails}).to_excel(output, index=False)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"emails_{ts}.xlsx",
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    elif file_type == 'json':
        result = {'emails': emails, 'timestamp': datetime.now().isoformat()}
        return create_download_response(json.dumps(result, indent=2, ensure_ascii=False), f"emails_{ts}.json")
    return "Geçersiz dosya tipi", 400

def create_download_response(content, filename):
    output = io.BytesIO()
    output.write(content.encode('utf-8'))
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=filename, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)