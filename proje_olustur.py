import os

# Proje klasör yapısını tanımlayalım
folders = ['templates', 'utils', 'uploads', 'static/css', 'static/js']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Dosya içerikleri
files = {
    'requirements.txt': """Flask==2.3.3
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
lxml==4.9.3
openpyxl==3.1.2
xlrd==2.0.1
urllib3==2.0.4
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.2
python-dotenv==1.0.0""",

    'static/css/style.css': """/* static/css/style.css */

/* Genel Stiller */
body {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Navbar */
.navbar {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
}

/* Kartlar */
.card {
    border: none;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s;
    margin-bottom: 20px;
}

.card:hover {
    transform: translateY(-5px);
}

.card-header {
    border-radius: 15px 15px 0 0 !important;
    font-weight: bold;
}

/* Butonlar */
.btn {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.3s;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.btn-lg {
    padding: 12px 30px;
    font-size: 1.1rem;
}

.btn-rounded {
    border-radius: 50px;
    padding: 10px 30px;
}

/* Tablolar */
.table {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.table thead th {
    background-color: #f8f9fa;
    border-bottom: 2px solid #dee2e6;
    font-weight: 600;
}

.table tbody tr:hover {
    background-color: rgba(0,123,255,0.05);
}

/* Alertler */
.alert {
    border-radius: 10px;
    border: none;
    padding: 15px 20px;
}

/* Badge'ler */
.badge {
    font-size: 0.8rem;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: 500;
}

/* Kod blokları */
code {
    color: #d63384;
    font-size: 0.9rem;
}

/* Progress bar */
.progress {
    height: 20px;
    margin: 5px 0;
    border-radius: 10px;
}

/* Tablo hücreleri */
.table td {
    vertical-align: middle;
}

/* Scroll Top Butonu */
#scrollTopBtn {
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    position: fixed;
    bottom: 20px;
    right: 20px;
    border-radius: 50px;
    padding: 10px 20px;
    z-index: 1000;
    display: none;
}

#scrollTopBtn:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

#scrollBottomBtn {
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    position: fixed;
    bottom: 75px;
    right: 20px;
    border-radius: 50px;
    padding: 10px 20px;
    z-index: 1000;
    display: block;
}

#scrollBottomBtn:hover {
    transform: translateY(5px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

/* Öncelik renkli kenarlıklar */
.border-danger { border-left: 4px solid #dc3545 !important; }
.border-warning { border-left: 4px solid #ffc107 !important; }
.border-info { border-left: 4px solid #0dcaf0 !important; }
.border-secondary { border-left: 4px solid #6c757d !important; }
.border-dark { border-left: 4px solid #212529 !important; }
.border-success { border-left: 4px solid #198754 !important; }
.border-primary { border-left: 4px solid #0d6efd !important; }

/* Scroll geçmişi */
.bg-light {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
}

/* Footer */
footer {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-top: 1px solid #dee2e6;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    h4 {
        font-size: 1.2rem;
    }
    
    .btn {
        padding: 8px 15px;
    }
    
    .table {
        font-size: 0.9rem;
    }
}

/* Animasyonlar */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.card, .alert, .table {
    animation: fadeInUp 0.6s ease-out;
}

/* Loading spinner */
.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* Tablo hover */
.table-hover tbody tr:hover {
    background-color: rgba(0,123,255,0.1);
    cursor: pointer;
}

/* Dosya yükleme alanı */
.file-upload {
    border: 2px dashed #dee2e6;
    border-radius: 10px;
    padding: 30px;
    text-align: center;
    background: #f8f9fa;
    transition: all 0.3s;
    cursor: pointer;
}

.file-upload:hover {
    border-color: #0d6efd;
    background: #e9ecef;
}

.file-upload.dragover {
    border-color: #28a745;
    background: #e8f5e9;
}

/* Dosya listesi */
.file-list {
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 10px;
    margin-top: 10px;
}

.file-item {
    display: flex;
    align-items: center;
    padding: 5px 10px;
    border-bottom: 1px solid #f0f0f0;
}

.file-item:last-child {
    border-bottom: none;
}

.file-item i {
    margin-right: 10px;
    color: #0d6efd;
}

.file-item .file-name {
    flex: 1;
    font-size: 0.9rem;
}

.file-item .file-size {
    color: #6c757d;
    font-size: 0.8rem;
    margin-right: 10px;
}

.file-item .remove-file {
    color: #dc3545;
    cursor: pointer;
    transition: all 0.3s;
}

.file-item .remove-file:hover {
    transform: scale(1.2);
}

/* Bildirim */
.notification-alert {
    animation: slideIn 0.3s ease-out;
    z-index: 9999;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* İstatistik kartları */
.stat-card {
    transition: all 0.3s;
}

.stat-card:hover {
    transform: scale(1.05);
}

/* Domain badge'leri */
.domain-badge {
    background-color: #e9ecef;
    color: #495057;
    padding: 3px 8px;
    border-radius: 15px;
    font-size: 0.75rem;
}

/* Çoklu dosya seçim göstergesi */
.multi-file-badge {
    background-color: #28a745;
    color: white;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-left: 10px;
}""",

    'static/js/script.js': """// static/js/script.js

// Sayfa yüklendiğinde çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeFileUpload();
    initializeMultiFileUpload();
    updateTimestamp();
    setupScrollButton();
    setupFormValidation();
    setupDragAndDrop();
});

// Tooltips başlatma
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Tekli dosya yükleme
function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]:not([multiple])');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = this.files.length > 0 ? this.files[0].name : 'Dosya seçilmedi';
            const fileLabel = this.nextElementSibling;
            if (fileLabel && fileLabel.classList.contains('file-name')) {
                fileLabel.textContent = fileName;
            }
        });
    });
}

// Çoklu dosya yükleme
function initializeMultiFileUpload() {
    const multiFileInputs = document.querySelectorAll('input[type="file"][multiple]');
    
    multiFileInputs.forEach(input => {
        const container = document.createElement('div');
        container.className = 'file-list mt-2';
        container.id = `file-list-${Math.random().toString(36).substr(2, 9)}`;
        input.parentNode.insertBefore(container, input.nextSibling);
        
        const counter = document.createElement('span');
        counter.className = 'multi-file-badge badge bg-success';
        counter.style.display = 'none';
        input.parentNode.insertBefore(counter, input.nextSibling);
        
        input.addEventListener('change', function(e) {
            updateFileList(this, container, counter);
        });
    });
}

function updateFileList(input, container, counter) {
    const files = Array.from(input.files);
    
    if (files.length === 0) {
        container.innerHTML = '';
        counter.style.display = 'none';
        return;
    }
    
    counter.textContent = `${files.length} dosya seçildi`;
    counter.style.display = 'inline-block';
    
    let html = '<div class="file-list-header d-flex justify-content-between align-items-center mb-2">';
    html += '<small class="text-muted">Seçilen dosyalar:</small>';
    html += '<button type="button" class="btn btn-sm btn-link text-danger clear-files">Temizle</button>';
    html += '</div>';
    
    files.forEach((file, index) => {
        const size = formatFileSize(file.size);
        html += `
            <div class="file-item" data-index="${index}">
                <i class="bi bi-file-earmark"></i>
                <span class="file-name">${file.name}</span>
                <span class="file-size">${size}</span>
                <i class="bi bi-x-circle remove-file" data-index="${index}"></i>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    container.querySelector('.clear-files')?.addEventListener('click', function() {
        input.value = '';
        container.innerHTML = '';
        counter.style.display = 'none';
    });
    
    container.querySelectorAll('.remove-file').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = parseInt(this.dataset.index);
            removeFileFromInput(input, index, container, counter);
        });
    });
}

function removeFileFromInput(input, index, container, counter) {
    const dt = new DataTransfer();
    const files = Array.from(input.files);
    
    files.forEach((file, i) => {
        if (i !== index) {
            dt.items.add(file);
        }
    });
    
    input.files = dt.files;
    updateFileList(input, container, counter);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function setupDragAndDrop() {
    const dropZones = document.querySelectorAll('.file-upload');
    
    dropZones.forEach(zone => {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            zone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, unhighlight, false);
        });
        
        zone.addEventListener('drop', handleDrop, false);
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    e.target.classList.add('dragover');
}

function unhighlight(e) {
    e.target.classList.remove('dragover');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    const fileInput = e.target.closest('.file-upload')?.querySelector('input[type="file"]');
    
    if (fileInput) {
        if (fileInput.multiple) {
            const newDt = new DataTransfer();
            const existingFiles = Array.from(fileInput.files);
            existingFiles.forEach(file => newDt.items.add(file));
            Array.from(files).forEach(file => newDt.items.add(file));
            fileInput.files = newDt.files;
        } else {
            fileInput.files = files;
        }
        
        const event = new Event('change', { bubbles: true });
        fileInput.dispatchEvent(event);
    }
}

function updateTimestamp() {
    const timestampElements = document.querySelectorAll('[data-timestamp]');
    timestampElements.forEach(elem => {
        const now = new Date();
        const formatted = now.toLocaleString('tr-TR');
        elem.textContent = formatted;
    });
}

function setupScrollButton() {
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    const scrollBottomBtn = document.getElementById('scrollBottomBtn');

    function updateButtons() {
        const scrolled = document.body.scrollTop > 300 || document.documentElement.scrollTop > 300;
        const atBottom = (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50;

        if (scrollTopBtn) scrollTopBtn.style.display = scrolled ? 'block' : 'none';
        if (scrollBottomBtn) scrollBottomBtn.style.display = atBottom ? 'none' : 'block';
    }

    window.addEventListener('scroll', updateButtons);
    updateButtons();
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToBottom() {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const fileInputs = this.querySelectorAll('input[type="file"]');
            let hasFile = false;
            
            fileInputs.forEach(input => {
                if (input.files.length > 0) hasFile = true;
            });
            
            if (this.querySelector('input[type="url"]')) {
                const urlInput = this.querySelector('input[type="url"]');
                if (urlInput && !urlInput.value) {
                    e.preventDefault();
                    showNotification('Lütfen bir URL girin!', 'warning');
                }
            }
            
            if (fileInputs.length > 0 && !hasFile) {
                e.preventDefault();
                showNotification('Lütfen en az bir dosya seçin!', 'warning');
            }
        });
    });
}

function showNotification(message, type = 'info') {
    const oldAlert = document.querySelector('.notification-alert');
    if (oldAlert) oldAlert.remove();
    
    const alert = document.createElement('div');
    alert.className = `notification-alert alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        if (alert && alert.parentNode) {
            alert.remove();
        }
    }, 3000);
}

function setExampleUrl(url) {
    const urlInput = document.getElementById('url_input');
    if (urlInput) {
        urlInput.value = url;
    }
}""",

    'app.py': """from flask import Flask, render_template, request, send_file
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
    
    content = '\\n'.join(all_content)
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    url_pattern = r'https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+[^\\s<>"{}|\\\\^`\\[\\]]*|www\\.[^\\s<>"{}|\\\\^`\\[\\]]+'
    
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
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    
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
        content = '\\n'.join(emails)
        return create_download_response(content, f"emails_{ts}.txt")
    elif file_type == 'urls':
        content = '\\n'.join(urls)
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
        return create_download_response('\\n'.join(emails), f"emails_{ts}.txt")
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
    app.run(debug=True, host='0.0.0.0', port=5000)""",

    'utils/__init__.py': """from .email_extractor import *
from .url_extractor import *
from .web_scraper import *""",

    'utils/email_extractor.py': """import re
from bs4 import BeautifulSoup

def extract_emails_from_text(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    json_email_pattern = r'"email"\\s*:\\s*"([^"]+)"'
    json_emails = re.findall(json_email_pattern, text)
    all_emails = set(emails + json_emails)
    return sorted(all_emails)

def extract_emails_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    mailto_emails = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('mailto:'):
            email = href.replace('mailto:', '').split('?')[0]
            mailto_emails.append(email)
    text_emails = extract_emails_from_text(soup.get_text())
    html_emails = extract_emails_from_text(html_content)
    all_emails = set(mailto_emails + text_emails + html_emails)
    return sorted(all_emails)""",

    'utils/url_extractor.py': """import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def extract_urls_from_text(text):
    url_pattern = r'https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+[^\\s<>"{}|\\\\^`\\[\\]]*|www\\.[^\\s<>"{}|\\\\^`\\[\\]]+'
    urls = re.findall(url_pattern, text)
    json_url_pattern = r'"url"\\s*:\\s*"([^"]+)"'
    json_urls = re.findall(json_url_pattern, text)
    all_urls = set(urls + json_urls)
    return sorted(all_urls)

def extract_urls_from_html(html_content, base_url=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href and not href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
            if base_url and not href.startswith(('http://', 'https://')):
                href = urljoin(base_url, href)
            urls.add(href)
    for img in soup.find_all('img', src=True):
        src = img['src']
        if base_url and not src.startswith(('http://', 'https://')):
            src = urljoin(base_url, src)
        urls.add(src)
    return sorted(urls)

def extract_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        domain = domain.replace('www.', '')
        return domain.split('/')[0]
    except:
        return ''""",

    'utils/web_scraper.py': """import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, urljoin
from .email_extractor import extract_emails_from_html
from .url_extractor import extract_urls_from_html

def scrape_website(url, max_pages=1, delay=1):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    all_emails = set()
    all_urls = set()
    visited_urls = set()
    main_html = None
    
    def should_visit(url):
        try:
            base_domain = urlparse(base_url).netloc
            url_domain = urlparse(url).netloc
            return base_domain == url_domain and url not in visited_urls
        except:
            return False
    
    def scrape_page(page_url, depth=0):
        nonlocal main_html
        if page_url in visited_urls or depth >= max_pages:
            return
        visited_urls.add(page_url)
        try:
            if depth > 0:
                time.sleep(delay)
            response = requests.get(page_url, headers=headers, timeout=30)
            response.raise_for_status()
            html_content = response.text
            if depth == 0:
                main_html = html_content
            all_emails.update(extract_emails_from_html(html_content))
            all_urls.update(extract_urls_from_html(html_content, page_url))
            if depth < max_pages - 1:
                for link in BeautifulSoup(html_content, 'html.parser').find_all('a', href=True):
                    href = link['href']
                    if href and not href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                        full_url = urljoin(page_url, href)
                        if should_visit(full_url):
                            scrape_page(full_url, depth + 1)
        except Exception as e:
            print(f"Hata: {e}")
    
    base_url = url if url.startswith(('http://', 'https://')) else 'https://' + url
    scrape_page(base_url)
    return main_html, sorted(all_emails), sorted(all_urls)

def scrape_paginated_website(base_url, start_page=1, end_page=10, delay=1):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    all_emails = set()
    all_urls = set()
    scraped_pages = []
    
    for page in range(start_page, end_page + 1):
        if '{page}' in base_url:
            url = base_url.replace('{page}', str(page))
        elif '?' in base_url:
            url = f"{base_url}&page={page}"
        else:
            url = f"{base_url}?page={page}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            html_content = response.text
            page_emails = extract_emails_from_html(html_content)
            page_urls = extract_urls_from_html(html_content, url)
            
            all_emails.update(page_emails)
            all_urls.update(page_urls)
            
            scraped_pages.append({
                'page': page,
                'url': url,
                'email_count': len(page_emails),
                'url_count': len(page_urls)
            })
            
            if page < end_page:
                time.sleep(delay)
                
        except Exception as e:
            scraped_pages.append({
                'page': page,
                'url': url,
                'error': str(e)
            })
    
    return sorted(all_emails), sorted(all_urls), scraped_pages""",

    'templates/base.html': """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Email & URL Scraper{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">📧 Email & URL Scraper</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/">Ana Sayfa</a></li>
                    <li class="nav-item"><a class="nav-link" href="/paginated-scan"><i class="bi bi-files"></i> Sayfalı Tarama</a></li>
                    <li class="nav-item"><a class="nav-link" href="/url-to-email"><i class="bi bi-envelope-plus"></i> URL'den Email</a></li>
                    <li class="nav-item"><a class="nav-link" href="/excel-email-merger"><i class="bi bi-file-earmark-spreadsheet"></i> Excel Birleştir</a></li>
                    <li class="nav-item"><a class="nav-link" href="/about">Hakkında</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <main class="container my-4">{% block content %}{% endblock %}</main>
    <footer class="bg-light py-3 mt-5"><div class="container text-center"><p class="text-muted mb-0"><i class="bi bi-envelope"></i> Email & URL Scraper v2.0 - Sayfalı Tarama Eklendi</p></div></footer>
    <button onclick="scrollToTop()" id="scrollTopBtn" class="btn btn-primary"><i class="bi bi-arrow-up"></i> Yukarı</button>
    <button onclick="scrollToBottom()" id="scrollBottomBtn" class="btn btn-secondary"><i class="bi bi-arrow-down"></i> Aşağı</button>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>""",

    'templates/index.html': """{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4>Email ve URL Çıkarıcı</h4>
            </div>
            <div class="card-body">
                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item">
                        <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#url">URL'den Çek</button>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#file">Dosya Yükle</button>
                    </li>
                </ul>
                
                <div class="tab-content mt-3">
                    <div class="tab-pane fade show active" id="url">
                        <form action="/extract" method="post">
                            <div class="mb-3">
                                <label>Web Sitesi URL'si:</label>
                                <input type="url" class="form-control" name="url_input" required>
                            </div>
                            <div class="mb-3">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="deep_scan">
                                    <label>Derin tarama (alt sayfaları da tara)</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="save_html">
                                    <label>HTML kaynağını kaydet</label>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary">Tarama Başlat</button>
                        </form>
                    </div>
                    
                    <div class="tab-pane fade" id="file">
                        <form action="/extract" method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label class="fw-bold">Dosyaları Seç (Birden çok seçilebilir):</label>
                                <div class="file-upload p-4 text-center border rounded mt-2">
                                    <i class="bi bi-cloud-upload fs-1 d-block"></i>
                                    <p class="mb-2">Dosyaları sürükleyip bırakın veya tıklayın</p>
                                    <input type="file" class="d-none" id="file-input" name="files" accept=".txt,.html,.htm,.csv,.json" multiple required>
                                    <button type="button" class="btn btn-outline-primary" onclick="document.getElementById('file-input').click()">Dosya Seç</button>
                                </div>
                                <small class="text-muted d-block mt-2">Desteklenen formatlar: TXT, HTML, CSV, JSON</small>
                            </div>
                            <button type="submit" class="btn btn-primary">Dosyaları İşle</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.getElementById('file-input').addEventListener('change', function(e) {
    const fileCount = this.files.length;
    if (fileCount > 0) {
        const btn = document.querySelector('.file-upload button');
        btn.innerHTML = `<i class="bi bi-check-circle"></i> ${fileCount} dosya seçildi`;
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-success');
    }
});
</script>
{% endblock %}""",

    'templates/results.html': """{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header bg-success text-white">
                <h4>Sonuçlar - {{ results.timestamp }}</h4>
            </div>
            <div class="card-body">
                {% if error %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% else %}
                    <div class="alert alert-info">
                        <i class="bi bi-files"></i> 
                        <strong>İşlenen:</strong> 
                        {% if results.source == 'url' %}
                            {{ results.files[0] }}
                        {% else %}
                            {{ results.files|length }} dosya
                        {% endif %}
                    </div>
                    
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5>📧 Email</h5>
                                    <h2>{{ results.emails|length }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5>🔗 URL</h5>
                                    <h2>{{ results.urls|length }}</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    {% if results.emails %}
                    <h5>Email Adresleri ({{ results.emails|length }}):</h5>
                    <div class="mb-3" style="max-height: 300px; overflow-y: auto; border: 1px solid #dee2e6; border-radius: 5px; padding: 10px;">
                        {% for email in results.emails[:50] %}
                            <span class="badge bg-primary mb-1">{{ email }}</span>
                        {% endfor %}
                        {% if results.emails|length > 50 %}
                            <div class="text-muted mt-2">... ve {{ results.emails|length - 50 }} email daha</div>
                        {% endif %}
                    </div>
                    
                    <form action="/download" method="POST" style="display: inline;">
                        <input type="hidden" name="type" value="emails">
                        <input type="hidden" name="result_key" value="{{ results.result_key }}">
                        <button type="submit" class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-file-text"></i> Email İndir (TXT)
                        </button>
                    </form>
                    
                    <button onclick="copyEmails({{ results.emails|tojson }})" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-clipboard"></i> Email Kopyala
                    </button>
                    {% endif %}
                    
                    {% if results.urls %}
                    <h5 class="mt-3">URL'ler ({{ results.urls|length }}):</h5>
                    <div class="mb-3" style="max-height: 300px; overflow-y: auto; border: 1px solid #dee2e6; border-radius: 5px; padding: 10px;">
                        {% for url in results.urls[:20] %}
                            <div><a href="{{ url }}" target="_blank">{{ url }}</a></div>
                        {% endfor %}
                        {% if results.urls|length > 20 %}
                            <div class="text-muted mt-2">... ve {{ results.urls|length - 20 }} URL daha</div>
                        {% endif %}
                    </div>
                    
                    <form action="/download" method="POST" style="display: inline;">
                        <input type="hidden" name="type" value="urls">
                        <input type="hidden" name="result_key" value="{{ results.result_key }}">
                        <button type="submit" class="btn btn-sm btn-outline-success">
                            <i class="bi bi-file-text"></i> URL İndir (TXT)
                        </button>
                    </form>
                    
                    <button onclick="copyUrls({{ results.urls|tojson }})" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-clipboard"></i> URL Kopyala
                    </button>
                    {% endif %}
                    
                    {% if results.emails and results.urls %}
                    <div class="mt-3">
                        <form action="/download" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="csv">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-success">
                                <i class="bi bi-file-spreadsheet"></i> CSV İndir
                            </button>
                        </form>
                        
                        <form action="/download" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="json">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-warning">
                                <i class="bi bi-file-code"></i> JSON İndir
                            </button>
                        </form>
                        
                        <button onclick="copyAll({{ results.emails|tojson }}, {{ results.urls|tojson }})" class="btn btn-outline-info">
                            <i class="bi bi-clipboard"></i> Tümünü Kopyala
                        </button>
                    </div>
                    {% endif %}
                    
                    <div class="mt-4">
                        <a href="/" class="btn btn-primary">
                            <i class="bi bi-arrow-left"></i> Yeni Dosya Yükle
                        </a>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<script>
function copyEmails(emails) {
    const text = emails.join('\\n');
    navigator.clipboard.writeText(text).then(() => {
        alert(`${emails.length} email panoya kopyalandı!`);
    });
}

function copyUrls(urls) {
    const text = urls.join('\\n');
    navigator.clipboard.writeText(text).then(() => {
        alert(`${urls.length} URL panoya kopyalandı!`);
    });
}

function copyAll(emails, urls) {
    let text = "=== EMAIL ADRESLERİ ===\\n";
    text += emails.join('\\n');
    text += "\\n\\n=== URL'LER ===\\n";
    text += urls.join('\\n');
    navigator.clipboard.writeText(text).then(() => {
        alert('Tüm veriler panoya kopyalandı!');
    });
}
</script>
{% endblock %}""",

    'templates/paginated_scan.html': """{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-md-10 mx-auto">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4><i class="bi bi-files"></i> Sayfalı Site Tarayıcı</h4>
            </div>
            <div class="card-body">
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    <strong>Nasıl Çalışır:</strong> Sayfalı yapıdaki siteleri tarar (OSTİM gibi).
                    <ul class="mb-0 mt-2">
                        <li>🔗 Örnek: <code>https://www.ostim.org.tr/firma-urunler?page=1</code></li>
                        <li>📊 1'den X'e kadar tüm sayfaları tarar</li>
                        <li>📧 Tüm sayfalardaki email adreslerini toplar</li>
                        <li>🔗 Tüm sayfalardaki URL'leri toplar</li>
                        <li>⏱️ Sayfalar arasında gecikme ayarlanabilir</li>
                    </ul>
                </div>

                {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
                {% endif %}

                <form method="post" action="/scan-paginated">
                    <div class="mb-3">
                        <label class="fw-bold">Base URL:</label>
                        <input type="url" class="form-control" name="base_url" 
                               value="https://www.ostim.org.tr/firma-urunler?page=1" 
                               placeholder="https://example.com/list?page=1" required>
                        <div class="form-text">Sayfa numarası parametresi olan URL (page=1 ile biten)</div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="fw-bold">Başlangıç Sayfası:</label>
                                <input type="number" class="form-control" name="start_page" value="1" min="1" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="fw-bold">Bitiş Sayfası:</label>
                                <input type="number" class="form-control" name="end_page" value="10" min="1" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="fw-bold">Sayfalar Arası Gecikme (saniye):</label>
                        <input type="number" class="form-control" name="delay" value="1" min="0.5" step="0.5">
                        <div class="form-text">Siteyi yormamak için sayfalar arasında bekleme süresi</div>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-search"></i> Taramayı Başlat
                    </button>
                    <a href="/" class="btn btn-secondary">Ana Sayfa</a>
                </form>
            </div>
        </div>

        {% if results %}
        <div class="card mt-4" id="sonuclar">
            <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="bi bi-check-circle"></i> Tarama Sonuçları</h5>
                <span class="badge bg-light text-dark">
                    <i class="bi bi-files"></i> {{ results.start_page }}-{{ results.end_page }} arası
                </span>
            </div>
            <div class="card-body">
                <div class="alert alert-success">
                    <i class="bi bi-link"></i> <strong>Taranan Site:</strong> {{ results.base_url }}
                </div>

                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>📊 Taranan Sayfa</h6>
                                <h3>{{ results.scraped_pages|length }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>📧 Toplam Email</h6>
                                <h3>{{ results.emails|length }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>🔗 Toplam URL</h6>
                                <h3>{{ results.urls|length }}</h3>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mb-4">
                    <h6>📋 Sayfa Bazlı Sonuçlar:</h6>
                    <div class="table-responsive">
                        <table class="table table-sm table-striped">
                            <thead class="table-dark">
                                <tr>
                                    <th>Sayfa</th>
                                    <th>Email Sayısı</th>
                                    <th>URL Sayısı</th>
                                    <th>Durum</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for page in results.scraped_pages %}
                                <tr>
                                    <td>{{ page.page }}</td>
                                    <td>{{ page.email_count|default(0) }}</td>
                                    <td>{{ page.url_count|default(0) }}</td>
                                    <td>
                                        {% if page.error %}
                                            <span class="badge bg-danger">Hata</span>
                                        {% else %}
                                            <span class="badge bg-success">Başarılı</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>

                {% if results.emails %}
                <div class="mb-3">
                    <h6>📧 Bulunan Email Adresleri ({{ results.emails|length }}):</h6>
                    <div class="bg-light p-3 rounded" style="max-height: 200px; overflow-y: auto;">
                        {% for email in results.emails %}
                            <span class="badge bg-primary mb-1">{{ email }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}

                {% if results.urls %}
                <div class="mb-3">
                    <h6>🔗 Bulunan URL'ler ({{ results.urls|length }}):</h6>
                    <div class="bg-light p-3 rounded" style="max-height: 200px; overflow-y: auto;">
                        {% for url in results.urls[:50] %}
                            <div><a href="{{ url }}" target="_blank">{{ url }}</a></div>
                        {% endfor %}
                        {% if results.urls|length > 50 %}
                            <div class="text-muted mt-2">... ve {{ results.urls|length - 50 }} URL daha</div>
                        {% endif %}
                    </div>
                </div>
                {% endif %}

                <div class="mt-4">
                    <div class="btn-group">
                        <form action="/download" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="emails">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-primary">
                                <i class="bi bi-file-text"></i> Email İndir (TXT)
                            </button>
                        </form>
                        <form action="/download" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="urls">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-success">
                                <i class="bi bi-file-text"></i> URL İndir (TXT)
                            </button>
                        </form>
                        <form action="/download" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="csv">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-info">
                                <i class="bi bi-file-spreadsheet"></i> CSV İndir
                            </button>
                        </form>
                    </div>
                </div>
            </div>
            <div class="card-footer text-center bg-light">
                <button onclick="scrollToTop()" class="btn btn-primary btn-rounded">
                    <i class="bi bi-arrow-up-circle-fill"></i> Sayfa Başına
                </button>
                <a href="/paginated-scan" class="btn btn-info btn-rounded">
                    <i class="bi bi-plus-circle"></i> Yeni Tarama
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}""",

    'templates/url_to_email_converter.html': """{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-md-10 mx-auto">
        <div class="card">
            <div class="card-header bg-info text-white">
                <h4><i class="bi bi-envelope-plus"></i> URL'den Email Oluşturucu</h4>
            </div>
            <div class="card-body">
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    <strong>Nasıl Çalışır:</strong> Yüklenen dosyadaki URL'leri öncelik sırasına göre info@ email'lerine dönüştürür.
                    <ol class="mb-0 mt-2">
                        <li><span class="badge bg-danger">Öncelik 1</span> https://www. → info@domain</li>
                        <li><span class="badge bg-warning">Öncelik 2</span> http://www. → info@domain</li>
                        <li><span class="badge bg-info">Öncelik 3</span> https:// → info@domain</li>
                        <li><span class="badge bg-secondary">Öncelik 4</span> http:// → info@domain</li>
                        <li><span class="badge bg-dark">Öncelik 5</span> www. → info@domain</li>
                    </ol>
                </div>

                {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
                {% endif %}

                <form method="post" action="/convert-urls" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label class="fw-bold">Dosyaları Seç (Birden çok seçilebilir):</label>
                        <div class="file-upload p-4 text-center border rounded mt-2">
                            <i class="bi bi-cloud-upload fs-1 d-block"></i>
                            <p class="mb-2">Dosyaları sürükleyip bırakın veya tıklayın</p>
                            <input type="file" class="d-none" id="file-input" name="files" accept=".txt,.csv,.json" multiple required>
                            <button type="button" class="btn btn-outline-primary" onclick="document.getElementById('file-input').click()">Dosya Seç</button>
                        </div>
                        <small class="text-muted d-block mt-2">Desteklenen formatlar: TXT, CSV, JSON</small>
                    </div>
                    <button type="submit" class="btn btn-info"><i class="bi bi-arrow-repeat"></i> Dönüştür ve Bul</button> 
                    <a href="/" class="btn btn-secondary">Ana Sayfa</a>
                </form>
            </div>
        </div>

        {% if results %}
        <div class="card mt-4" id="sonuclar">
            <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="bi bi-check-circle"></i> Sonuçlar</h5>
                <span class="badge bg-light text-dark"><i class="bi bi-files"></i> {{ results.file_count }} dosya</span>
            </div>
            <div class="card-body">
                <div class="alert alert-success mb-4">
                    <i class="bi bi-files"></i> <strong>İşlenen Dosyalar:</strong>
                    <ul>
                        {% for file in results.files %}
                        <li>{{ file }}</li>
                        {% endfor %}
                    </ul>
                </div>

                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>📧 Bulunan Email</h6>
                                <h3>{{ results.emails|length }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>🔗 Bulunan URL</h6>
                                <h3>{{ results.found_urls }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>📨 Oluşturulan Email</h6>
                                <h3>{{ results.converted_emails|length }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>📊 Toplam</h6>
                                <h3>{{ results.emails|length + results.converted_emails|length }}</h3>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row mb-4">
                    <div class="col-md-2">
                        <div class="card border-danger">
                            <div class="card-body text-center p-2">
                                <h6>Öncelik 1</h6>
                                <h5 class="text-danger">{{ results.stats.priority1 }}</h5>
                                <small>https://www</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card border-warning">
                            <div class="card-body text-center p-2">
                                <h6>Öncelik 2</h6>
                                <h5 class="text-warning">{{ results.stats.priority2 }}</h5>
                                <small>http://www</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card border-info">
                            <div class="card-body text-center p-2">
                                <h6>Öncelik 3</h6>
                                <h5 class="text-info">{{ results.stats.priority3 }}</h5>
                                <small>https://</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card border-secondary">
                            <div class="card-body text-center p-2">
                                <h6>Öncelik 4</h6>
                                <h5 class="text-secondary">{{ results.stats.priority4 }}</h5>
                                <small>http://</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card border-dark">
                            <div class="card-body text-center p-2">
                                <h6>Öncelik 5</h6>
                                <h5 class="text-dark">{{ results.stats.priority5 }}</h5>
                                <small>www.</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card border-secondary">
                            <div class="card-body text-center p-2">
                                <h6>Diğer</h6>
                                <h5 class="text-muted">{{ results.stats.other }}</h5>
                                <small>dönüşmeyen</small>
                            </div>
                        </div>
                    </div>
                </div>

                {% if results.conversions %}
                <div class="mb-4">
                    <h6>🔍 Dönüştürülen URL'ler:</h6>
                    <div class="table-responsive">
                        <table class="table table-sm table-striped">
                            <thead class="table-dark">
                                <tr>
                                    <th>#</th>
                                    <th>Orijinal URL</th>
                                    <th>Öncelik</th>
                                    <th>Oluşturulan Email</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in results.conversions %}
                                <tr>
                                    <td>{{ loop.index }}</td>
                                    <td><small class="text-muted">{{ item.original[:80] }}{% if item.original|length > 80 %}...{% endif %}</small></td>
                                    <td>
                                        {% if item.priority == 1 %}
                                            <span class="badge bg-danger">1</span>
                                        {% elif item.priority == 2 %}
                                            <span class="badge bg-warning text-dark">2</span>
                                        {% elif item.priority == 3 %}
                                            <span class="badge bg-info">3</span>
                                        {% elif item.priority == 4 %}
                                            <span class="badge bg-secondary">4</span>
                                        {% elif item.priority == 5 %}
                                            <span class="badge bg-dark">5</span>
                                        {% endif %}
                                    </td>
                                    <td><strong class="text-primary">{{ item.converted }}</strong></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                {% endif %}

                {% if results.emails %}
                <div class="mb-3">
                    <h6>📧 Bulunan Email:</h6>
                    <div class="bg-light p-3 rounded" style="max-height: 150px; overflow-y: auto;">
                        {% for email in results.emails %}
                            <span class="badge bg-primary mb-1">{{ email }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}

                <div class="mb-3">
                    <h6>📨 Oluşturulan Email:</h6>
                    <div class="bg-light p-3 rounded" style="max-height: 150px; overflow-y: auto;">
                        {% for email in results.converted_emails %}
                            <code class="text-success d-block">{{ email }}</code>
                        {% endfor %}
                    </div>
                </div>

                <div class="mt-4">
                    <div class="btn-group">
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="txt">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-primary">
                                <i class="bi bi-file-text"></i> TXT İndir
                            </button>
                        </form>
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="csv">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-success">
                                <i class="bi bi-file-spreadsheet"></i> CSV İndir
                            </button>
                        </form>
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="excel">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-danger">
                                <i class="bi bi-file-earmark-excel"></i> Excel İndir
                            </button>
                        </form>
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="json">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-warning">
                                <i class="bi bi-file-code"></i> JSON İndir
                            </button>
                        </form>
                    </div>
                    <button onclick="copyEmails({{ results.converted_emails|tojson }})" class="btn btn-outline-secondary mt-2">
                        <i class="bi bi-clipboard"></i> Listeyi Kopyala
                    </button>
                </div>
            </div>
            <div class="card-footer text-center bg-light">
                <button onclick="scrollToTop()" class="btn btn-primary btn-rounded"><i class="bi bi-arrow-up-circle-fill"></i> Sayfa Başına</button>
            </div>
        </div>
        {% endif %}
    </div>
</div>

<script>
document.getElementById('file-input').addEventListener('change', function(e) {
    const fileCount = this.files.length;
    if (fileCount > 0) {
        const btn = document.querySelector('.file-upload button');
        btn.innerHTML = `<i class="bi bi-check-circle"></i> ${fileCount} dosya seçildi`;
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-success');
    }
});

function copyEmails(emails) {
    const text = emails.join('\\n');
    navigator.clipboard.writeText(text).then(() => {
        alert(`${emails.length} email panoya kopyalandı!`);
    });
}
</script>
{% endblock %}""",

    'templates/excel_email_merger.html': """{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-md-10 mx-auto">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4><i class="bi bi-file-earmark-spreadsheet"></i> Çoklu Excel Email Birleştirici</h4>
            </div>
            <div class="card-body">
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    <strong>Nasıl Çalışır:</strong> Birden çok Excel/CSV dosyası yükleyin, tüm email'leri bulup tekilleştirelim.
                    <ul>
                        <li>📊 Excel/CSV dosyaları taranır</li>
                        <li>📧 Email'ler otomatik bulunur</li>
                        <li>🔄 Aynı email'ler tekilleştirilir</li>
                        <li>📥 Sonuçları TXT, CSV, Excel, JSON olarak indirin</li>
                    </ul>
                </div>

                <form method="post" action="/merge-excel-emails" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label class="fw-bold">Excel/CSV Dosyalarını Seç (Çoklu seçim için Ctrl basılı tutun):</label>
                        <div class="file-upload p-4 text-center border rounded mt-2">
                            <i class="bi bi-cloud-upload fs-1 d-block"></i>
                            <p class="mb-2">Dosyaları sürükleyip bırakın veya tıklayın</p>
                            <input type="file" class="d-none" id="file-input" name="files" accept=".xlsx,.xls,.csv" multiple required>
                            <button type="button" class="btn btn-outline-primary" onclick="document.getElementById('file-input').click()">Dosya Seç</button>
                        </div>
                        <small class="text-muted d-block mt-2">Desteklenen formatlar: XLSX, XLS, CSV</small>
                    </div>
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="include_domains">
                            <label>Domain bazlı gruplama yap</label>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary"><i class="bi bi-diagram-3"></i> Birleştir</button> 
                    <a href="/" class="btn btn-secondary">Ana Sayfa</a>
                </form>
            </div>
        </div>

        {% if results %}
        <div class="card mt-4" id="sonuclar">
            <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="bi bi-check-circle"></i> Sonuçlar</h5>
                <span class="badge bg-light text-dark"><i class="bi bi-files"></i> {{ results.file_count }} dosya</span>
            </div>
            <div class="card-body">
                <div class="alert alert-success mb-4">
                    <i class="bi bi-files"></i> <strong>İşlenen Dosyalar:</strong>
                    <ul>
                        {% for file in results.files %}
                        <li>{{ file }}</li>
                        {% endfor %}
                    </ul>
                </div>

                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>📊 Toplam Hücre</h6>
                                <h3>{{ results.total_cells }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>📧 Benzersiz Email</h6>
                                <h3>{{ results.unique_emails|length }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card bg-light">
                            <div class="card-body text-center">
                                <h6>🔤 Domain Sayısı</h6>
                                <h3>{{ results.domains|length }}</h3>
                            </div>
                        </div>
                    </div>
                </div>

                {% if results.domain_stats %}
                <div class="mb-4">
                    <h6>Domain Dağılımı:</h6>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Domain</th>
                                <th>Sayı</th>
                                <th>Yüzde</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for domain, count in results.domain_stats.items() %}
                            <tr>
                                <td>@{{ domain }}</td>
                                <td>{{ count }}</td>
                                <td>
                                    <div class="progress">
                                        <div class="progress-bar" style="width: {{ (count/results.unique_emails|length*100)|round }}%">
                                            {{ (count/results.unique_emails|length*100)|round }}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endif %}

                <div class="mb-3">
                    <h6>📧 Email Listesi ({{ results.unique_emails|length }}):</h6>
                    <div class="bg-light p-3 rounded" style="max-height:300px;overflow-y:auto;">
                        {% for email in results.unique_emails %}
                            <code class="d-block">{{ email }}</code>
                        {% endfor %}
                    </div>
                </div>

                <div class="mt-4">
                    <div class="btn-group">
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="txt">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-primary">
                                <i class="bi bi-file-text"></i> TXT İndir
                            </button>
                        </form>
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="csv">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-success">
                                <i class="bi bi-file-spreadsheet"></i> CSV İndir
                            </button>
                        </form>
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="excel">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-danger">
                                <i class="bi bi-file-earmark-excel"></i> Excel İndir
                            </button>
                        </form>
                        <form action="/download-converted" method="POST" style="display: inline;">
                            <input type="hidden" name="type" value="json">
                            <input type="hidden" name="result_key" value="{{ results.result_key }}">
                            <button type="submit" class="btn btn-outline-warning">
                                <i class="bi bi-file-code"></i> JSON İndir
                            </button>
                        </form>
                    </div>
                    <button onclick="copyEmails({{ results.unique_emails|tojson }})" class="btn btn-outline-secondary mt-2">
                        <i class="bi bi-clipboard"></i> Listeyi Kopyala
                    </button>
                </div>
            </div>
            <div class="card-footer text-center bg-light">
                <button onclick="scrollToTop()" class="btn btn-primary btn-rounded"><i class="bi bi-arrow-up-circle-fill"></i> Sayfa Başına</button>
            </div>
        </div>
        {% endif %}
    </div>
</div>

<script>
document.getElementById('file-input').addEventListener('change', function(e) {
    const fileCount = this.files.length;
    if (fileCount > 0) {
        const btn = document.querySelector('.file-upload button');
        btn.innerHTML = `<i class="bi bi-check-circle"></i> ${fileCount} dosya seçildi`;
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-success');
    }
});

function copyEmails(emails) {
    const text = emails.join('\\n');
    navigator.clipboard.writeText(text).then(() => {
        alert(`${emails.length} email panoya kopyalandı!`);
    });
}
</script>
{% endblock %}""",

    'templates/about.html': """{% extends "base.html" %}
{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4>Hakkında</h4>
            </div>
            <div class="card-body">
                <h5>Email & URL Scraper</h5>
                <p>7 farklı script tek çatı altında:</p>
                <ul>
                    <li>baslik.py - Google arama</li>
                    <li>eposya.py - Email çıkarma</li>
                    <li>logo_scraper.py - Web scraping</li>
                    <li>mikro.py - HTML parsing</li>
                    <li>url.py / url2.py - URL çıkarma</li>
                </ul>
                <hr>
                <h6>URL'den Email Kuralları:</h6>
                <ol>
                    <li>https://www. → info@domain</li>
                    <li>http://www. → info@domain</li>
                    <li>https:// → info@domain</li>
                    <li>http:// → info@domain</li>
                    <li>www. → info@domain</li>
                </ol>
                <hr>
                <h6>Yeni Özellik - Sayfalı Tarama:</h6>
                <p>OSTİM gibi sayfalı yapıdaki siteleri tarayabilirsiniz.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
}

# Klasörleri oluştur
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Dosyaları oluştur
for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("✅ Tüm proje dosyaları başarıyla oluşturuldu!")
print("📁 Klasör yapısı:")
print("   - app.py")
print("   - requirements.txt")
print("   - utils/ (4 dosya)")
print("   - templates/ (7 dosya)")
print("   - static/css/ (1 dosya)")
print("   - static/js/ (1 dosya)")
print("   - uploads/ (boş klasör)")
print("\n🚀 YENİ ÖZELLİK: Sayfalı Tarama")
print("   OSTİM gibi siteler için: https://www.ostim.org.tr/firma-urunler?page=1")
print("\n📦 Çalıştırmak için:")
print("1. pip install -r requirements.txt")
print("2. python app.py")
print("3. http://localhost:5000")
print("4. 'Sayfalı Tarama' sekmesini dene!")