"""
proje_olustur.py
────────────────
Bu betik çalıştırıldığında projenin tüm klasör yapısını ve dosyalarını sıfırdan oluşturur.
Tek komutla kurulum: python proje_olustur.py
"""

import os  # Dosya/klasör işlemleri için standart kütüphane

# ────────────────────────────────────────────────────────────────────────────────
# KLASÖR YAPISI
# Proje çalışmadan önce bu klasörlerin mevcut olması gerekir.
# 'temp_results' geçici JSON sonuçlar için, 'uploads' yüklenen dosyalar için kullanılır.
# ────────────────────────────────────────────────────────────────────────────────
folders = [
    'templates',    # Jinja2 HTML şablonları
    'utils',        # Yardımcı Python modülleri
    'uploads',      # Kullanıcının yüklediği geçici dosyalar
    'static/css',   # Özel CSS stilleri
    'static/js',    # Özel JavaScript dosyaları
    'temp_results', # İşlem sonuçlarının geçici saklandığı yer (1 saat sonra temizlenir)
]

# Klasörler yoksa oluştur; varsa hata verme (exist_ok=True yerine manuel kontrol)
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ────────────────────────────────────────────────────────────────────────────────
# DOSYA İÇERİKLERİ
# Her anahtar bir dosya yolu, değeri ise o dosyanın içeriğidir.
# ────────────────────────────────────────────────────────────────────────────────
files = {

    # ══════════════════════════════════════════════════════════════
    # .env  –  Gizli anahtar ve ortam ayarları
    # Bu dosya asla Git'e eklenmemelidir (.gitignore'a ekle).
    # ══════════════════════════════════════════════════════════════
    '.env': """SECRET_KEY=buraya-guclu-rastgele-bir-anahtar-yaz
FLASK_ENV=development
MAX_UPLOAD_MB=50
""",

    # ══════════════════════════════════════════════════════════════
    # .env.example  –  Takım arkadaşları için şablon
    # Gerçek değerler yerine açıklayıcı yer tutucular içerir.
    # ══════════════════════════════════════════════════════════════
    '.env.example': """SECRET_KEY=BURAYI_DEGISTIR_EN_AZ_32_KARAKTER
FLASK_ENV=development
MAX_UPLOAD_MB=50
""",

    # ══════════════════════════════════════════════════════════════
    # .gitignore  –  Git'e gönderilmemesi gereken dosyalar
    # ══════════════════════════════════════════════════════════════
    '.gitignore': """.env
__pycache__/
*.pyc
*.pyo
uploads/
temp_results/
app.log
venv/
.venv/
*.egg-info/
dist/
build/
.DS_Store
""",

    # ══════════════════════════════════════════════════════════════
    # requirements.txt  –  Python bağımlılıkları
    # >= ile minimum sürüm belirtilir; == kullanmak kırılganlık yaratır.
    # ══════════════════════════════════════════════════════════════
    'requirements.txt': """Flask>=2.3.3
requests>=2.31.0
beautifulsoup4>=4.12.2
pandas>=2.0.3
lxml>=4.9.3
openpyxl>=3.1.2
xlrd>=2.0.1
urllib3>=2.0.4
Werkzeug>=2.3.7
Jinja2>=3.1.2
MarkupSafe>=2.1.3
itsdangerous>=2.1.2
click>=8.1.7
blinker>=1.6.2
python-dotenv>=1.0.0
python-magic>=0.4.27
""",

    # ══════════════════════════════════════════════════════════════
    # app.py  –  Ana Flask uygulaması
    # Tüm HTTP rotaları, iş mantığı koordinasyonu ve indirme işlemleri burada.
    # ══════════════════════════════════════════════════════════════
    'app.py': """\"\"\"
app.py  –  Email & URL Scraper – Ana Flask Uygulaması
─────────────────────────────────────────────────────
Sorumluluklar:
  • HTTP rotalarını tanımlamak
  • Kullanıcı girdilerini doğrulamak
  • utils modüllerini çağırıp sonuçları şablona aktarmak
  • Geçici dosya yönetimi ve indirme rotaları
\"\"\"

import os           # Dosya yolu ve ortam değişkeni işlemleri
import io           # Bellek içi dosya akışı (indirme için)
import re           # Düzenli ifadeler (e-posta/URL regex)
import json         # Geçici sonuçları JSON olarak kaydetme/okuma
import uuid         # Her sonuç seti için benzersiz anahtar üretme
import glob         # Geçici dosyaları listeleyip temizleme
import time         # Sayfalar arası gecikme ve dosya yaşı hesabı
import logging      # print() yerine yapılandırılmış loglama
from datetime import datetime  # Zaman damgaları

from flask import Flask, render_template, request, send_file, abort
from werkzeug.utils import secure_filename  # Güvenli dosya adı dönüşümü
import pandas as pd                         # Excel/CSV okuma ve yazma
from dotenv import load_dotenv              # .env dosyasını ortama yükle

# utils paketinden gerekli fonksiyonları açıkça içe aktar (wildcard import yok)
from utils.email_extractor import extract_emails_from_text, extract_emails_from_html
from utils.url_extractor import extract_urls_from_text, extract_urls_from_html
from utils.web_scraper import scrape_website, scrape_paginated_website
from utils.file_utils import allowed_file, safe_delete_upload

# ── Ortam değişkenleri ──────────────────────────────────────────────────────────
# .env dosyasındaki değerleri os.environ'a yükle
load_dotenv()

# ── Loglama yapılandırması ──────────────────────────────────────────────────────
# Hem konsola hem app.log dosyasına yaz; format: tarih [seviye] modül: mesaj
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),                              # Konsol çıktısı
        logging.FileHandler('app.log', encoding='utf-8'),    # Dosya çıktısı
    ]
)
logger = logging.getLogger(__name__)  # Bu modüle özgü logger nesnesi

# ── Flask uygulaması ────────────────────────────────────────────────────────────
app = Flask(__name__)

# SECRET_KEY: Oturum güvenliği için kullanılır; .env'den oku, bulunamazsa uyarı değeri kullan
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'degistir-beni')

# UPLOAD_FOLDER: Kullanıcıdan gelen dosyalar buraya kaydedilir, işlem sonrası silinir
app.config['UPLOAD_FOLDER'] = 'uploads'

# MAX_CONTENT_LENGTH: Maksimum yükleme boyutu (byte cinsinden); .env'den MB olarak alınır
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_MB', 50)) * 1024 * 1024

# Geçici sonuç klasörü; UUID'li JSON dosyaları burada tutulur
TEMP_FOLDER = 'temp_results'

# Uygulama başlarken klasörlerin var olduğundan emin ol
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)


# ── Geçici sonuç yönetimi ────────────────────────────────────────────────────────

def save_temp_results(data: dict) -> str:
    \"\"\"
    Sonuç verisini UUID adlı bir JSON dosyasına kaydeder.
    Aynı anda 1 saatten eski tüm geçici dosyaları da temizler.

    Args:
        data: Kaydedilecek sözlük (e-postalar, URL'ler, meta veriler)

    Returns:
        str: Oluşturulan dosyayı tanımlayan UUID anahtarı
    \"\"\"
    # 1 saatten (3600 saniye) eski geçici JSON dosyalarını sil
    for f in glob.glob(os.path.join(TEMP_FOLDER, '*.json')):
        try:
            if time.time() - os.path.getmtime(f) > 3600:
                os.remove(f)
        except OSError:
            pass  # Dosya zaten silinmişse sessizce geç

    # Benzersiz anahtar oluştur ve veriyi JSON olarak kaydet
    key = str(uuid.uuid4())
    path = os.path.join(TEMP_FOLDER, f"{key}.json")
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False)
    return key


def load_temp_results(key: str) -> dict:
    \"\"\"
    Daha önce kaydedilmiş geçici JSON sonucunu yükler.
    Path traversal saldırısına karşı UUID formatını doğrular.

    Args:
        key: save_temp_results() tarafından döndürülen UUID

    Returns:
        dict: Sonuç verisi; anahtar geçersiz veya dosya yoksa boş sözlük
    \"\"\"
    if not key:
        return {}  # Boş anahtar gelirse erken çık

    # Güvenlik: yalnızca geçerli UUID formatına izin ver (../../../etc/passwd gibi saldırıları engelle)
    if not re.fullmatch(r'[0-9a-f\\-]{36}', key):
        logger.warning("Geçersiz result_key formatı: %s", key)
        return {}

    path = os.path.join(TEMP_FOLDER, f"{key}.json")
    if not os.path.exists(path):
        return {}  # Dosya bulunamazsa boş dön (silinmiş veya süresi dolmuş olabilir)

    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


# ── Yardımcı fonksiyonlar ────────────────────────────────────────────────────────

def create_download_response(content: str, filename: str):
    \"\"\"
    Metin içeriğini bellek içi dosya olarak döndürür; tarayıcı indirir.

    Args:
        content: İndirilecek metin içerik
        filename: Tarayıcıda gösterilecek dosya adı

    Returns:
        Flask Response nesnesi
    \"\"\"
    output = io.BytesIO()              # Bellekte geçici dosya akışı oluştur
    output.write(content.encode('utf-8'))  # İçeriği UTF-8 olarak yaz
    output.seek(0)                     # Akışın başına dön (okuma için)
    return send_file(output, as_attachment=True, download_name=filename, mimetype='text/plain')


def user_friendly_error(e: Exception) -> str:
    \"\"\"
    Ham Python hata mesajını kullanıcıya göstermek yerine loglar,
    genel bir Türkçe mesaj döndürür. Bu sayede iç sistem detayları gizlenir.

    Args:
        e: Yakalanan exception nesnesi

    Returns:
        str: Kullanıcıya gösterilecek genel hata mesajı
    \"\"\"
    logger.error("İşlem hatası: %s", e, exc_info=True)  # Stack trace ile logla
    return "Bir hata oluştu. Lütfen tekrar deneyin."


# ── Sayfa rotaları ───────────────────────────────────────────────────────────────

@app.route('/')
def index():
    \"\"\"Ana sayfa – dosya yükleme veya URL girme formu.\"\"\"
    return render_template('index.html')


@app.route('/about')
def about():
    \"\"\"Hakkında sayfası – proje açıklaması ve scriptler.\"\"\"
    return render_template('about.html')


@app.route('/url-to-email')
def url_to_email_page():
    \"\"\"URL → E-posta dönüştürücü sayfası.\"\"\"
    return render_template('url_to_email_converter.html')


@app.route('/excel-email-merger')
def excel_email_merger_page():
    \"\"\"Excel/CSV birleştirici sayfası.\"\"\"
    return render_template('excel_email_merger.html')


@app.route('/paginated-scan')
def paginated_scan_page():
    \"\"\"Sayfalı site tarayıcı sayfası.\"\"\"
    return render_template('paginated_scan.html')


@app.route('/email-to-url')
def email_to_url_page():
    \"\"\"E-posta → URL dönüştürücü sayfası.\"\"\"
    return render_template('email_to_url.html')


# ── Ana çıkarma rotası ───────────────────────────────────────────────────────────

@app.route('/extract', methods=['POST'])
def extract():
    \"\"\"
    URL veya yüklenen dosyalardan e-posta ve URL çıkarır.
    İki mod:
      1. URL modu: Web sitesi taranır
      2. Dosya modu: Yüklenen dosyalar işlenir
    \"\"\"
    # Sonuç sözlüğünü başlat; her iki modda da bu yapı doldurulur
    results = {
        'emails': [],   # Bulunan e-posta adresleri
        'urls': [],     # Bulunan URL'ler
        'source': '',   # Kaynak türü: 'url' veya 'files'
        'files': [],    # İşlenen dosya/URL listesi
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # İşlem zamanı
    }

    # ── Mod 1: URL tarama ─────────────────────────────────────────
    if 'url_input' in request.form and request.form['url_input']:
        url = request.form['url_input']
        results['source'] = 'url'
        results['files'] = [url]
        try:
            # Form checkbox'larını kontrol et
            deep_scan = 'deep_scan' in request.form    # Alt sayfaları da tara
            save_html = 'save_html' in request.form    # HTML kaynağını kaydet

            # Derin taramada maks 5 sayfa, normal taramada 1 sayfa
            max_pages = 5 if deep_scan else 1

            # Web scraper modülünü çağır; html içeriği, e-postalar ve URL'leri döndürür
            html_content, emails, urls = scrape_website(url, max_pages=max_pages)
            results['emails'] = emails
            results['urls'] = urls

            # Kullanıcı HTML kaynağını kaydetmek istediyse uploads klasörüne yaz
            if save_html and html_content:
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                html_path = os.path.join(app.config['UPLOAD_FOLDER'], f"kaynak_{ts}.html")
                with open(html_path, 'w', encoding='utf-8') as hf:
                    hf.write(html_content)
                results['saved_html'] = f"kaynak_{ts}.html"  # Şablona bildir

        except Exception as e:
            # Hata kullanıcıya loglanmış genel mesaj olarak gösterilir
            return render_template('results.html', error=user_friendly_error(e))

    # ── Mod 2: Dosya yükleme ──────────────────────────────────────
    elif 'files' in request.files:
        files = request.files.getlist('files')  # Birden fazla dosya alınabilir

        # Hiç dosya seçilmediyse kullanıcıyı uyar
        if not files or files[0].filename == '':
            return render_template('index.html', error="Dosya seçilmedi"), 400

        all_emails, all_urls = set(), set()  # Tekrarları önlemek için küme kullan
        file_list = []

        for file in files:
            if not file or not file.filename:
                continue  # Boş dosya nesnesini atla

            # Uzantı kontrolü: izin verilmeyen tipler reddedilir
            if not allowed_file(file.filename):
                logger.warning("İzin verilmeyen dosya tipi: %s", file.filename)
                continue

            # Güvenli dosya adı üret (../../../etc gibi path traversal önlenir)
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)   # Geçici olarak diske kaydet
            file_list.append(filename)

            try:
                ext = filename.rsplit('.', 1)[1].lower()  # Uzantıyı al

                # Dosyayı UTF-8 ile oku; hatalı karakterleri yoksay
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # HTML dosyaları için özel parser; diğerleri için düz metin regex
                if ext in ('html', 'htm'):
                    all_emails.update(extract_emails_from_html(content))
                    all_urls.update(extract_urls_from_html(content))
                else:
                    all_emails.update(extract_emails_from_text(content))
                    all_urls.update(extract_urls_from_text(content))

            except Exception as e:
                logger.error("Dosya işleme hatası (%s): %s", filename, e)
            finally:
                # Başarı veya hata fark etmeksizin geçici dosyayı sil (disk birikimine karşı)
                safe_delete_upload(filepath)

        results['source'] = 'files'
        results['files'] = file_list
        results['emails'] = sorted(all_emails)  # Alfabetik sırala
        results['urls'] = sorted(all_urls)

    # Sonuçları geçici JSON dosyasına kaydet; indirme için anahtar şablona geçilir
    results['result_key'] = save_temp_results(results)
    return render_template('results.html', results=results)


# ── Sayfalı tarama rotası ────────────────────────────────────────────────────────

@app.route('/scan-paginated', methods=['POST'])
def scan_paginated():
    \"\"\"
    ?page=N parametreli URL'leri belirli bir aralıkta sırayla tarar.
    Örnek: https://ostim.org.tr/firmalar?page=1 → page=1'den page=20'ye kadar
    \"\"\"
    base_url = request.form.get('base_url', '').strip()
    if not base_url:
        return render_template('paginated_scan.html', error="Lütfen bir URL girin!")

    try:
        # Sayfa numaralarını integer'a çevir; geçersizse ValueError yakala
        start_page = max(1, int(request.form.get('start_page', 1)))
        # Güvenlik: en fazla 100 sayfa taranabilir (start + 99)
        end_page = min(int(request.form.get('end_page', 1)), start_page + 99)
        # Güvenlik: sayfalar arası en az 0.5 saniye bekle (ban önleme)
        delay = max(0.5, float(request.form.get('delay', 1)))
    except ValueError:
        return render_template('paginated_scan.html',
                               error="Geçersiz sayfa numarası veya gecikme değeri!")

    try:
        # Scraper modülünü çağır; tüm sayfalardaki e-posta ve URL'leri toplar
        all_emails, all_urls, scraped_pages = scrape_paginated_website(
            base_url, start_page, end_page, delay
        )
        results = {
            'base_url': base_url,
            'start_page': start_page,
            'end_page': end_page,
            'scraped_pages': scraped_pages,    # Her sayfanın istatistiği
            'emails': sorted(all_emails),
            'urls': sorted(all_urls),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        results['result_key'] = save_temp_results(results)
        return render_template('paginated_scan.html', results=results)
    except Exception as e:
        return render_template('paginated_scan.html', error=user_friendly_error(e))


# ── Derlenen regex sabitleri ─────────────────────────────────────────────────────
# Modül seviyesinde bir kez derlenir; her istek için yeniden derlenmez (performans)

# E-posta adresi örüntüsü: kullanici@alan.tld
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}')

# URL örüntüsü: http(s):// ile başlayanlar veya www. ile başlayanlar
URL_RE = re.compile(
    r'https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+[^\\s<>"{}|\\\\^`\\[\\]]*'
    r'|www\\.[^\\s<>"{}|\\\\^`\\[\\]]+'
)


# ── URL → E-posta dönüştürme rotası ─────────────────────────────────────────────

@app.route('/convert-urls', methods=['POST'])
def convert_urls():
    \"\"\"
    Yüklenen dosyalardaki URL'leri 'info@domain.com' formatında e-postalara çevirir.
    5 öncelik seviyesine göre dönüşüm yapılır:
      1. https://www.  →  en güvenilir
      5. www.          →  en düşük öncelik
    \"\"\"
    if 'files' not in request.files:
        return render_template('url_to_email_converter.html', error="Dosya seçilmedi")

    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return render_template('url_to_email_converter.html', error="Dosya seçilmedi")

    all_content, file_list = [], []

    # Tüm dosyaları oku, içerikleri birleştir
    for file in files:
        if not file or not file.filename:
            continue
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_list.append(filename)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                all_content.append(f.read())
        except Exception as e:
            logger.error("Dosya okuma hatası (%s): %s", filename, e)
        finally:
            safe_delete_upload(filepath)  # Geçici dosyayı temizle

    # Birleştirilmiş içerikten e-posta ve URL'leri çıkar
    content = '\\n'.join(all_content)
    found_emails = list(set(EMAIL_RE.findall(content)))
    found_urls   = list(set(URL_RE.findall(content)))

    conversions, converted_emails = [], []

    # Öncelik sırası: en spesifik prefix önce kontrol edilir
    priority_map = [
        ('https://www.', 1),   # En güvenilir: HTTPS + www
        ('http://www.',  2),   # HTTP + www
        ('https://',     3),   # HTTPS, www olmadan
        ('http://',      4),   # HTTP, www olmadan
        ('www.',         5),   # Sadece www
    ]

    stats = {f'priority{i}': 0 for i in range(1, 6)}  # Her öncelik için sayaç
    stats['other'] = 0  # Hiçbir prefix ile eşleşmeyenler

    for url in found_urls:
        domain, priority = None, 0
        # URL'in hangi prefix ile başladığını bul
        for prefix, prio in priority_map:
            if url.startswith(prefix):
                # Domain'i çıkar: prefix'i kaldır, ilk '/' veya '?' de kes
                domain = url[len(prefix):].split('/')[0].split('?')[0]
                priority = prio
                break

        if domain:
            converted = f"info@{domain}"  # Varsayılan e-posta formatı
            stats[f'priority{priority}'] += 1
            conversions.append({
                'original': url,
                'converted': converted,
                'priority': priority,
                'domain': domain,
            })
            converted_emails.append(converted)
        else:
            stats['other'] += 1  # Tanınan prefix yok

    results = {
        'emails': found_emails,
        'found_urls': len(found_urls),
        'converted_emails': sorted(set(converted_emails)),   # Tekrarsız sıralı liste
        'conversions': sorted(conversions, key=lambda x: x['priority']),  # Önceliğe göre sırala
        'stats': stats,
        'files': file_list,
        'file_count': len(file_list),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    results['result_key'] = save_temp_results(results)
    return render_template('url_to_email_converter.html', results=results)


# ── Excel e-posta birleştirme rotası ────────────────────────────────────────────

@app.route('/merge-excel-emails', methods=['POST'])
def merge_excel_emails():
    \"\"\"
    Birden fazla Excel (.xlsx, .xls) veya CSV dosyasını birleştirir.
    Tüm sütunlardaki e-posta adreslerini bulur, tekrarları temizler.
    \"\"\"
    if 'files' not in request.files:
        return render_template('excel_email_merger.html', error="Dosya seçilmedi"), 400

    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return render_template('excel_email_merger.html', error="Dosya seçilmedi"), 400

    # Domain bazlı istatistik isteği (opsiyonel form checkbox)
    include_domains = 'include_domains' in request.form

    all_emails: set = set()   # Tüm dosyalardaki benzersiz e-postalar
    file_list, total_cells = [], 0

    for file in files:
        if not file or not file.filename:
            continue
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_list.append(filename)

        try:
            # CSV ve Excel dosyaları için farklı okuyucu kullan
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
            else:
                df = pd.read_excel(filepath)

            # Tüm sütunlardaki tüm hücreleri tara
            for col in df.columns:
                for val in df[col].dropna():  # Boş hücreleri atla
                    total_cells += 1
                    # Hücre değerini stringe çevirip e-posta ara
                    for em in EMAIL_RE.findall(str(val)):
                        all_emails.add(em.lower())  # Küçük harfe normalize et
        except Exception as e:
            logger.error("Excel okuma hatası (%s): %s", filename, e)
        finally:
            safe_delete_upload(filepath)

    unique_emails = sorted(all_emails)

    # Domain bazlı istatistik oluştur
    domain_stats = {}
    for em in unique_emails:
        dom = em.split('@')[1]
        domain_stats[dom] = domain_stats.get(dom, 0) + 1

    results = {
        'files': file_list,
        'file_count': len(file_list),
        'total_cells': total_cells,
        'unique_emails': unique_emails,
        'domains': sorted(domain_stats.keys()),
        'domain_stats': domain_stats if include_domains else None,  # Opsiyonel
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    results['result_key'] = save_temp_results(results)
    return render_template('excel_email_merger.html', results=results)


# ── E-posta → URL dönüştürme rotası ────────────────────────────────────────────

@app.route('/convert-emails-to-urls', methods=['POST'])
def convert_emails_to_urls():
    \"\"\"
    E-posta adreslerini domain bazlı URL'lere dönüştürür.
    Kaynak: dosya yükleme veya metin girişi.
    Her e-posta için 3 URL formatı üretilir:
      • https://www.domain.com
      • https://domain.com
      • http://www.domain.com
    \"\"\"
    found_emails, file_list = [], []

    # ── Dosya modu ─────────────────────────────────────────────────
    if 'files' in request.files:
        for file in request.files.getlist('files'):
            if not file or not file.filename:
                continue
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_list.append(filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    found_emails.extend(EMAIL_RE.findall(f.read()))
            except Exception as e:
                logger.error("Dosya okuma hatası (%s): %s", filename, e)
            finally:
                safe_delete_upload(filepath)

    # ── Metin girişi modu ──────────────────────────────────────────
    elif request.form.get('text_input', '').strip():
        found_emails = EMAIL_RE.findall(request.form['text_input'])
        file_list = ['(metin girişi)']

    # Tekrarlananları kaldır ve küçük harfe normalize et
    unique_emails = sorted(set(e.lower() for e in found_emails))

    # Her e-posta için 3 farklı URL formatı oluştur
    conversions = [
        {
            'email': em,
            'url_https_www': f"https://www.{em.split('@')[1]}",   # En yaygın format
            'url_https':     f"https://{em.split('@')[1]}",        # www olmadan
            'url_http_www':  f"http://www.{em.split('@')[1]}",     # Eski HTTP
        }
        for em in unique_emails
    ]

    results = {
        'files': file_list,
        'file_count': len(file_list),
        'total_emails': len(unique_emails),
        'conversions': conversions,
        'all_urls': sorted({c['url_https_www'] for c in conversions}),  # Benzersiz URL listesi
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    results['result_key'] = save_temp_results(results)
    return render_template('email_to_url.html', results=results)


# ── İndirme rotaları ────────────────────────────────────────────────────────────

@app.route('/download', methods=['POST'])
def download():
    \"\"\"
    Ana çıkarma sonuçlarını (e-posta ve URL) farklı formatlarda indirir.
    Desteklenen formatlar: txt (sadece e-postalar), url-txt, csv, json
    \"\"\"
    key = request.form.get('result_key', '')         # Geçici dosya anahtarı
    file_type = request.form.get('type', 'txt')      # İstenen format
    data = load_temp_results(key)

    if not data:
        abort(404)  # Anahtar geçersiz veya süresi dolmuş

    emails = data.get('emails', [])
    urls   = data.get('urls', [])
    ts     = datetime.now().strftime('%Y%m%d_%H%M%S')  # Dosya adı için zaman damgası

    if file_type == 'emails':
        return create_download_response('\\n'.join(emails), f"emails_{ts}.txt")

    if file_type == 'urls':
        return create_download_response('\\n'.join(urls), f"urls_{ts}.txt")

    if file_type == 'csv':
        # E-posta ve URL'leri yan yana iki sütuna yaz; boş hücreler '' ile doldurulur
        max_len = max(len(emails), len(urls), 1)
        df = pd.DataFrame({
            'Email': emails + [''] * (max_len - len(emails)),
            'URL':   urls   + [''] * (max_len - len(urls)),
        })
        out = io.BytesIO()
        df.to_csv(out, index=False, encoding='utf-8-sig')  # utf-8-sig: Excel Türkçe uyumu
        out.seek(0)
        return send_file(out, as_attachment=True, download_name=f"results_{ts}.csv",
                         mimetype='text/csv')

    if file_type == 'json':
        result = {'emails': emails, 'urls': urls, 'timestamp': datetime.now().isoformat()}
        return create_download_response(
            json.dumps(result, indent=2, ensure_ascii=False), f"results_{ts}.json"
        )

    return "Geçersiz dosya tipi", 400  # Bilinmeyen format isteği


@app.route('/download-converted', methods=['POST'])
def download_converted():
    \"\"\"
    URL→E-posta veya Excel birleştirme dönüşüm sonuçlarını indirir.
    Desteklenen formatlar: txt, csv, excel, json
    \"\"\"
    key = request.form.get('result_key', '')
    file_type = request.form.get('type', 'txt')
    data = load_temp_results(key)

    if not data:
        abort(404)

    # converted_emails varsa onu kullan, yoksa unique_emails'e bak
    emails = data.get('converted_emails', data.get('unique_emails', []))
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')

    if file_type == 'txt':
        return create_download_response('\\n'.join(emails), f"emails_{ts}.txt")

    if file_type == 'csv':
        out = io.BytesIO()
        pd.DataFrame({'Email': emails}).to_csv(out, index=False, encoding='utf-8-sig')
        out.seek(0)
        return send_file(out, as_attachment=True, download_name=f"emails_{ts}.csv",
                         mimetype='text/csv')

    if file_type == 'excel':
        out = io.BytesIO()
        pd.DataFrame({'Email': emails}).to_excel(out, index=False)
        out.seek(0)
        return send_file(out, as_attachment=True, download_name=f"emails_{ts}.xlsx",
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if file_type == 'json':
        result = {'emails': emails, 'timestamp': datetime.now().isoformat()}
        return create_download_response(
            json.dumps(result, indent=2, ensure_ascii=False), f"emails_{ts}.json"
        )

    return "Geçersiz dosya tipi", 400


@app.route('/download-e2u', methods=['POST'])
def download_e2u():
    \"\"\"
    E-posta → URL dönüşüm sonuçlarını indirir.
    Her satırda email + üç farklı URL formatı bulunur.
    Desteklenen formatlar: txt, csv, excel, json
    \"\"\"
    key = request.form.get('result_key', '')
    file_type = request.form.get('type', 'txt')
    data = load_temp_results(key)

    if not data:
        abort(404)

    conversions = data.get('conversions', [])
    urls        = data.get('all_urls', [])
    ts          = datetime.now().strftime('%Y%m%d_%H%M%S')

    if file_type == 'txt':
        return create_download_response('\\n'.join(urls), f"urls_{ts}.txt")

    if file_type in ('csv', 'excel'):
        # Her dönüşüm kaydını tablo satırına çevir
        rows = [
            {
                'Email': c['email'],
                'https://www.': c['url_https_www'],
                'https://':     c['url_https'],
                'http://www.':  c['url_http_www'],
            }
            for c in conversions
        ]
        df  = pd.DataFrame(rows)
        out = io.BytesIO()
        if file_type == 'csv':
            df.to_csv(out, index=False, encoding='utf-8-sig')
            out.seek(0)
            return send_file(out, as_attachment=True, download_name=f"email_to_url_{ts}.csv",
                             mimetype='text/csv')
        # Excel formatı
        df.to_excel(out, index=False)
        out.seek(0)
        return send_file(out, as_attachment=True, download_name=f"email_to_url_{ts}.xlsx",
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    if file_type == 'json':
        result = {'conversions': conversions, 'urls': urls, 'timestamp': datetime.now().isoformat()}
        return create_download_response(
            json.dumps(result, indent=2, ensure_ascii=False), f"email_to_url_{ts}.json"
        )

    return "Geçersiz dosya tipi", 400


# ── Uygulama giriş noktası ───────────────────────────────────────────────────────

if __name__ == '__main__':
    # FLASK_ENV=development ise debug modu açık; production'da kapalı olmalı
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=5000)
""",

    # ══════════════════════════════════════════════════════════════
    # utils/__init__.py  –  Açık import tanımları
    # Wildcard import (* from module) yerine her isim açıkça listelenir.
    # Bu sayede hangi fonksiyonun hangi modülden geldiği nettir.
    # ══════════════════════════════════════════════════════════════
    'utils/__init__.py': """\"\"\"
utils/__init__.py
─────────────────
utils paketinin dışa aktarma listesi.
Wildcard import ('from module import *') kullanılmaz;
hangi fonksiyonun kullanılabilir olduğu burada açıkça tanımlanır.
\"\"\"

# E-posta çıkarma fonksiyonları
from .email_extractor import extract_emails_from_text, extract_emails_from_html

# URL çıkarma ve domain ayrıştırma fonksiyonları
from .url_extractor import extract_urls_from_text, extract_urls_from_html, extract_domain

# Web scraping fonksiyonları (tek sayfa ve sayfalı tarama)
from .web_scraper import scrape_website, scrape_paginated_website

# Dosya doğrulama ve güvenli silme yardımcıları
from .file_utils import allowed_file, safe_delete_upload
""",

    # ══════════════════════════════════════════════════════════════
    # utils/file_utils.py  –  Dosya güvenliği yardımcıları
    # ══════════════════════════════════════════════════════════════
    'utils/file_utils.py': """\"\"\"
utils/file_utils.py
────────────────────
Yüklenen dosyaların uzantı doğrulaması ve geçici dosyaların
güvenli silinmesini sağlayan yardımcı fonksiyonlar.
\"\"\"

import os
import logging

logger = logging.getLogger(__name__)

# İzin verilen dosya uzantıları (küçük harf)
# Bu liste dışındaki dosyalar reddedilir.
ALLOWED_EXTENSIONS = {'txt', 'html', 'htm', 'csv', 'json', 'xlsx', 'xls'}


def allowed_file(filename: str) -> bool:
    \"\"\"
    Dosya adının uzantısını izin verilenler listesinde kontrol eder.

    Args:
        filename: Kontrol edilecek dosya adı (örn. 'veri.csv')

    Returns:
        bool: Uzantı izin verilenler listesindeyse True, değilse False

    Örnek:
        allowed_file('liste.txt')   # → True
        allowed_file('virus.exe')   # → False
        allowed_file('noext')       # → False (uzantı yok)
    \"\"\"
    if '.' not in filename:
        return False  # Uzantısız dosyalar reddedilir

    # rsplit ile son noktadan böl; yalnızca uzantıyı al
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def safe_delete_upload(filepath: str) -> None:
    \"\"\"
    İşlenmiş geçici dosyayı diskten güvenle siler.
    Dosya zaten silinmişse veya bulunamazsa sessizce devam eder.

    Args:
        filepath: Silinecek dosyanın tam yolu

    Neden gerekli?
        Yüklenen dosyalar işlendikten sonra sunucuda bırakılırsa
        disk dolabilir ve kullanıcı verisi gereksiz yere saklanmış olur.
    \"\"\"
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            # Silme işlemi başarılı (debug seviyesinde loglanabilir)
    except OSError as e:
        # Silme başarısız olursa uyarı logla ama uygulamayı çökertme
        logger.warning("Dosya silinemedi (%s): %s", filepath, e)
""",

    # ══════════════════════════════════════════════════════════════
    # utils/email_extractor.py  –  E-posta çıkarma motoru
    # ══════════════════════════════════════════════════════════════
    'utils/email_extractor.py': """\"\"\"
utils/email_extractor.py
─────────────────────────
Düz metinden, HTML içeriğinden ve JSON verilerinden
e-posta adresi çıkarmaya yarayan fonksiyonlar.

Yöntemler:
  1. Regex: Standart e-posta formatını yakalar
  2. Mailto: HTML'deki <a href='mailto:...'> bağlantıları
  3. JSON: 'email' anahtarlı JSON alanları
\"\"\"

import re
from bs4 import BeautifulSoup

# Standart e-posta adresi örüntüsü
# Yakalar: kullanici.adi+etiket@alt.alan.com gibi karmaşık adresleri de kapsar
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}')

# JSON içindeki "email": "..." alanlarını yakalar
JSON_EMAIL_RE = re.compile(r'"email"\\s*:\\s*"([^"]+)"')


def extract_emails_from_text(text: str) -> list:
    \"\"\"
    Düz metin içinden e-posta adreslerini çıkarır.
    Hem standart e-posta örüntüsünü hem JSON alanlarını tarar.

    Args:
        text: Taranacak düz metin

    Returns:
        list: Sıralanmış, benzersiz e-posta adresleri

    Örnek:
        extract_emails_from_text('info@ornek.com ile iletişime geçin')
        # → ['info@ornek.com']
    \"\"\"
    emails = EMAIL_RE.findall(text)           # Regex ile e-posta bul
    json_emails = JSON_EMAIL_RE.findall(text) # JSON alanlarından e-posta bul
    # İkisini birleştir, tekrarları kaldır, sırala
    return sorted(set(emails + json_emails))


def extract_emails_from_html(html_content: str) -> list:
    \"\"\"
    HTML belgesi içinden e-posta adreslerini çıkarır.
    Üç katmanlı arama yapar:
      1. <a href='mailto:...'> bağlantıları (en güvenilir)
      2. HTML'nin görünür metnindeki e-postalar
      3. Ham HTML kaynağındaki e-postalar (gizli alanlarda da arar)

    Args:
        html_content: Ham HTML string

    Returns:
        list: Sıralanmış, benzersiz e-posta adresleri
    \"\"\"
    # BeautifulSoup ile HTML'yi ayrıştır (lxml parser daha hızlı)
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Mailto bağlantılarını tara
    mailto_emails = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('mailto:'):
            # 'mailto:info@ornek.com?subject=Merhaba' → 'info@ornek.com'
            email = href.replace('mailto:', '').split('?')[0].strip()
            if email:
                mailto_emails.append(email)

    # 2. Görünür metinden e-posta çıkar (javascript render edilmemiş içerik)
    text_emails = extract_emails_from_text(soup.get_text())

    # 3. Ham HTML'den e-posta çıkar (data attribute'larında gizli olabilir)
    html_emails = extract_emails_from_text(html_content)

    # Tüm kaynakları birleştir, tekrarları kaldır, sırala
    return sorted(set(mailto_emails + text_emails + html_emails))
""",

    # ══════════════════════════════════════════════════════════════
    # utils/url_extractor.py  –  URL çıkarma motoru
    # ══════════════════════════════════════════════════════════════
    'utils/url_extractor.py': """\"\"\"
utils/url_extractor.py
───────────────────────
Düz metin ve HTML içeriğinden URL çıkarma,
ayrıca domain ayrıştırma fonksiyonları.
\"\"\"

import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# URL örüntüsü: http(s):// veya www. ile başlayan, boşluk/özel karakter içermeyen
URL_RE = re.compile(
    r'https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+[^\\s<>"{}|\\\\^`\\[\\]]*'
    r'|www\\.[^\\s<>"{}|\\\\^`\\[\\]]+'
)

# JSON içindeki "url": "..." alanlarını yakalar
JSON_URL_RE = re.compile(r'"url"\\s*:\\s*"([^"]+)"')

# Bu scheme'lerle başlayan href'ler URL değil; atlanır
SKIP_SCHEMES = ('mailto:', 'tel:', 'javascript:', '#')


def extract_urls_from_text(text: str) -> list:
    \"\"\"
    Düz metin içinden URL'leri çıkarır.
    Hem standart URL örüntüsünü hem JSON alanlarını tarar.

    Args:
        text: Taranacak düz metin

    Returns:
        list: Sıralanmış, benzersiz URL listesi
    \"\"\"
    urls = URL_RE.findall(text)           # Regex ile URL bul
    json_urls = JSON_URL_RE.findall(text) # JSON alanlarından URL bul
    return sorted(set(urls + json_urls))


def extract_urls_from_html(html_content: str, base_url: str = None) -> list:
    \"\"\"
    HTML belgesindeki tüm bağlantı ve görsel URL'lerini çıkarır.
    Göreceli URL'ler (href='/sayfa') varsa base_url ile mutlaklaştırılır.

    Args:
        html_content: Ham HTML string
        base_url: Göreceli URL'leri mutlaklaştırmak için kök adres (opsiyonel)

    Returns:
        list: Sıralanmış, benzersiz URL listesi
    \"\"\"
    soup = BeautifulSoup(html_content, 'html.parser')
    urls: set = set()

    # <a href='...'> bağlantılarını tara
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not href or href.startswith(SKIP_SCHEMES):
            continue  # Geçersiz veya e-posta/telefon bağlantısı; atla

        # Göreceli URL'yi mutlaklaştır (base_url verilmişse)
        if base_url and not href.startswith(('http://', 'https://')):
            href = urljoin(base_url, href)
        urls.add(href)

    # <img src='...'> görsel bağlantılarını tara
    for img in soup.find_all('img', src=True):
        src = img['src']
        if base_url and not src.startswith(('http://', 'https://')):
            src = urljoin(base_url, src)
        urls.add(src)

    return sorted(urls)


def extract_domain(url: str) -> str:
    \"\"\"
    URL'den temiz domain adını çıkarır.
    'www.' öneki kaldırılır; sadece alan adı döndürülür.

    Args:
        url: Tam URL (örn. 'https://www.ornek.com/sayfa?q=1')

    Returns:
        str: Temiz domain (örn. 'ornek.com'); hata varsa boş string

    Örnek:
        extract_domain('https://www.google.com/search') # → 'google.com'
    \"\"\"
    try:
        parsed = urlparse(url)
        # netloc: 'www.ornek.com'; path: göreceli URL'lerde dolu olabilir
        domain = parsed.netloc or parsed.path
        return domain.replace('www.', '').split('/')[0]
    except Exception:
        return ''  # Ayrıştırma başarısız; boş döndür
""",

    # ══════════════════════════════════════════════════════════════
    # utils/web_scraper.py  –  Web scraping motoru
    # ══════════════════════════════════════════════════════════════
    'utils/web_scraper.py': """\"\"\"
utils/web_scraper.py
─────────────────────
Web sitelerini tarayıp e-posta ve URL toplayan scraping motoru.
İki mod:
  1. scrape_website      – Tek site, isteğe bağlı alt sayfa taraması
  2. scrape_paginated_website – ?page=N yapılı sayfalı siteler
\"\"\"

import time
import logging
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from .email_extractor import extract_emails_from_html
from .url_extractor import extract_urls_from_html

logger = logging.getLogger(__name__)

# Tarayıcı gibi davranmak için User-Agent başlığı
# Bazı siteler bot gibi görünen istekleri reddeder; bu başlık engellenmeyi azaltır
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


def _normalize_url(url: str) -> str:
    \"\"\"
    URL'e scheme yoksa 'https://' ekler.

    Args:
        url: Ham URL (örn. 'ornek.com' veya 'https://ornek.com')

    Returns:
        str: Tam URL
    \"\"\"
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url


def scrape_website(url: str, max_pages: int = 1, delay: float = 1.0):
    \"\"\"
    Bir web sitesini (isteğe bağlı alt sayfalarıyla birlikte) tarar.
    Aynı domain dışına çıkmaz; ziyaret edilmiş sayfaları tekrar taramaz.

    Args:
        url: Başlangıç URL'i
        max_pages: Maksimum taranacak sayfa sayısı (1 = yalnızca verilen sayfa)
        delay: Sayfalar arası bekleme süresi (saniye)

    Returns:
        tuple: (ana_sayfa_html, e-posta_listesi, url_listesi)
    \"\"\"
    base_url = _normalize_url(url)
    base_domain = urlparse(base_url).netloc  # Yalnızca bu domain içinde kal

    all_emails: set = set()  # Tüm sayfalardan toplanan benzersiz e-postalar
    all_urls: set   = set()  # Tüm sayfalardan toplanan benzersiz URL'ler
    visited: set    = set()  # Ziyaret edilmiş sayfalar (sonsuz döngü önleme)
    main_html       = None   # İlk sayfanın HTML içeriği (kaydetmek için)

    def should_visit(candidate: str) -> bool:
        \"\"\"
        Verilen URL'nin taranması gerekip gerekmediğini belirler.
        Yalnızca aynı domain ve daha önce ziyaret edilmemiş sayfalar True döner.

        NOT: base_domain, dış kapsamdan (closure) alınır ve önceden tanımlanmıştır.
             Bu, eski sürümdeki 'tanımsız değişken' hatasını çözer.
        \"\"\"
        try:
            return (urlparse(candidate).netloc == base_domain   # Aynı domain mi?
                    and candidate not in visited)                # Daha önce ziyaret edilmedi mi?
        except Exception:
            return False  # URL ayrıştırılamazsa atla

    def scrape_page(page_url: str, depth: int = 0):
        \"\"\"
        Tek bir sayfayı tarar; alt sayfalara özyinelemeli iner.

        Args:
            page_url: Taranacak sayfa URL'i
            depth: Mevcut derinlik (max_pages ile sınırlandırılır)
        \"\"\"
        nonlocal main_html  # Dış scope'taki main_html'i güncelleyebilmek için

        # Aynı sayfa iki kez taranmasın; derinlik sınırı aşılmasın
        if page_url in visited or depth >= max_pages:
            return
        visited.add(page_url)

        try:
            # İlk sayfa değilse sayfalar arası bekle (sunucuya yük bindirmeme)
            if depth > 0:
                time.sleep(delay)

            # HTTP GET isteği gönder; 30 saniye zaman aşımı
            resp = requests.get(page_url, headers=HEADERS, timeout=30)
            resp.raise_for_status()  # 4xx/5xx durumlarında istisna fırlat
            html = resp.text

            # İlk sayfanın HTML'ini kaydet (kullanıcı isterse indirabilir)
            if depth == 0:
                main_html = html

            # Bu sayfadaki e-posta ve URL'leri topla
            all_emails.update(extract_emails_from_html(html))
            all_urls.update(extract_urls_from_html(html, page_url))

            # Derin tarama aktifse alt sayfaları da tara
            if depth < max_pages - 1:
                for link in BeautifulSoup(html, 'html.parser').find_all('a', href=True):
                    href = link['href']
                    if not href or href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                        continue
                    full = urljoin(page_url, href)  # Göreceli URL'yi mutlaklaştır
                    if should_visit(full):
                        scrape_page(full, depth + 1)  # Özyinelemeli alt sayfa tarama

        except requests.RequestException as e:
            # Ağ hatalarını logla ama uygulamayı çökertme
            logger.warning("Sayfa tarama hatası (%s): %s", page_url, e)

    # Ana sayfadan başla
    scrape_page(base_url)
    return main_html, sorted(all_emails), sorted(all_urls)


def scrape_paginated_website(base_url: str, start_page: int = 1,
                              end_page: int = 10, delay: float = 1.0):
    \"\"\"
    Sayfalı yapıdaki siteleri belirtilen aralıkta tarar.
    URL'de sayfa parametresi üç farklı şekilde eklenir:
      • '{page}' placeholder varsa: yerine sayı yazılır
      • '?' varsa: '&page=N' eklenir
      • Yoksa: '?page=N' eklenir

    Args:
        base_url:   Temel URL (sayfa numarası içermeli veya içermemeli)
        start_page: Başlangıç sayfa numarası
        end_page:   Bitiş sayfa numarası (dahil)
        delay:      Sayfalar arası bekleme süresi (saniye)

    Returns:
        tuple: (e-posta_kümesi, url_kümesi, sayfa_istatistikleri_listesi)
    \"\"\"
    all_emails: set = set()
    all_urls: set   = set()
    scraped_pages   = []  # Her sayfa için istatistik kaydı

    for page in range(start_page, end_page + 1):
        # Sayfa URL'sini oluştur: placeholder → sayı değiştir veya parametre ekle
        if '{page}' in base_url:
            url = base_url.replace('{page}', str(page))  # Özel placeholder
        elif '?' in base_url:
            url = f"{base_url}&page={page}"  # Zaten query string var; ek parametre
        else:
            url = f"{base_url}?page={page}"  # İlk query string parametresi

        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            html = resp.text

            # Bu sayfadaki e-posta ve URL'leri çıkar
            page_emails = extract_emails_from_html(html)
            page_urls   = extract_urls_from_html(html, url)
            all_emails.update(page_emails)
            all_urls.update(page_urls)

            # Sayfa istatistiğini kaydet
            scraped_pages.append({
                'page':        page,
                'url':         url,
                'email_count': len(page_emails),
                'url_count':   len(page_urls),
            })

        except requests.RequestException as e:
            logger.warning("Sayfa %d tarama hatası: %s", page, e)
            # Hata olan sayfayı istatistiğe hata mesajıyla ekle
            scraped_pages.append({'page': page, 'url': url, 'error': str(e)})

        # Son sayfa değilse bekle (sunucuya aşırı yük bindirmeme)
        if page < end_page:
            time.sleep(delay)

    return sorted(all_emails), sorted(all_urls), scraped_pages
""",

    # ══════════════════════════════════════════════════════════════
    # static/css/style.css  –  Özel stiller
    # Bootstrap üzerine eklenen özelleştirmeler
    # ══════════════════════════════════════════════════════════════
    'static/css/style.css': """/* ── Genel sayfa düzeni ────────────────────────────────────────── */
body {
    /* Yumuşak degrade arka plan; tüm ekran yüksekliğini kaplar */
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ── Navigasyon çubuğu ─────────────────────────────────────────── */
.navbar { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.navbar-brand { font-weight: bold; font-size: 1.5rem; }

/* ── Kart bileşenleri ──────────────────────────────────────────── */
.card {
    border: none;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s;   /* Hover animasyonu için geçiş */
    margin-bottom: 20px;
}
/* Karta hover'da hafif yukarı kalkma efekti */
.card:hover { transform: translateY(-5px); }
.card-header { border-radius: 15px 15px 0 0 !important; font-weight: bold; }

/* ── Butonlar ──────────────────────────────────────────────────── */
.btn {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.3s;
}
/* Hover'da yukarı kalkma + gölge efekti */
.btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
.btn-lg  { padding: 12px 30px; font-size: 1.1rem; }
.btn-rounded { border-radius: 50px; padding: 10px 30px; } /* Oval buton */

/* ── Tablolar ──────────────────────────────────────────────────── */
.table { border-radius: 10px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
.table thead th { background-color: #f8f9fa; border-bottom: 2px solid #dee2e6; font-weight: 600; }
.table tbody tr:hover { background-color: rgba(0,123,255,0.05); }

/* ── Uyarı kutuları ────────────────────────────────────────────── */
.alert { border-radius: 10px; border: none; padding: 15px 20px; }

/* ── Etiketler (badge) ─────────────────────────────────────────── */
.badge { font-size: 0.8rem; padding: 5px 10px; border-radius: 5px; font-weight: 500; }

/* ── Kod öğeleri ───────────────────────────────────────────────── */
code { color: #d63384; font-size: 0.9rem; }

/* ── İlerleme çubuğu ──────────────────────────────────────────── */
.progress { height: 20px; margin: 5px 0; border-radius: 10px; }
.table td { vertical-align: middle; }

/* ── Sayfanın başına/sonuna kaydırma butonları ─────────────────── */
/* Sağ alt köşede sabit konumda durur; scroll ile görünür/gizlenir */
#scrollTopBtn {
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    position: fixed; bottom: 20px; right: 20px;
    border-radius: 50px; padding: 10px 20px; z-index: 1000;
    display: none; /* JS tarafından kontrol edilir */
}
#scrollTopBtn:hover { transform: translateY(-5px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
#scrollBottomBtn {
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    position: fixed; bottom: 75px; right: 20px;
    border-radius: 50px; padding: 10px 20px; z-index: 1000;
    display: block; /* Sayfa yüklendiğinde görünür */
}
#scrollBottomBtn:hover { transform: translateY(5px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }

/* ── Sol kenarlık renkleri (kart vurgusu) ──────────────────────── */
.border-danger    { border-left: 4px solid #dc3545 !important; }
.border-warning   { border-left: 4px solid #ffc107 !important; }
.border-info      { border-left: 4px solid #0dcaf0 !important; }
.border-secondary { border-left: 4px solid #6c757d !important; }
.border-dark      { border-left: 4px solid #212529 !important; }
.border-success   { border-left: 4px solid #198754 !important; }
.border-primary   { border-left: 4px solid #0d6efd !important; }

/* ── Açık arka plan degrade ────────────────────────────────────── */
.bg-light { background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important; }

/* ── Alt bilgi (footer) ────────────────────────────────────────── */
footer { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-top: 1px solid #dee2e6; }

/* ── Mobil uyumluluk (responsive) ─────────────────────────────── */
@media (max-width: 768px) {
    .container { padding: 10px; }
    h4 { font-size: 1.2rem; }
    .btn { padding: 8px 15px; }
    .table { font-size: 0.9rem; }
}

/* ── Sayfa yükleme animasyonu ──────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card, .alert, .table { animation: fadeInUp 0.6s ease-out; }

/* ── Yükleniyor spinner ────────────────────────────────────────── */
.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%; width: 40px; height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

/* ── Özel kaydırma çubuğu ──────────────────────────────────────── */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 5px; }
::-webkit-scrollbar-thumb { background: #888; border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: #555; }

/* ── Tablo hover efekti ────────────────────────────────────────── */
.table-hover tbody tr:hover { background-color: rgba(0,123,255,0.1); cursor: pointer; }

/* ── Dosya yükleme alanı (drag & drop) ────────────────────────── */
.file-upload {
    border: 2px dashed #dee2e6;
    border-radius: 10px; padding: 30px; text-align: center;
    background: #f8f9fa; transition: all 0.3s; cursor: pointer;
}
.file-upload:hover  { border-color: #0d6efd; background: #e9ecef; }
/* Dosya sürüklendiğinde yeşil kenarlık */
.file-upload.dragover { border-color: #28a745; background: #e8f5e9; }

/* ── Seçilen dosya listesi ─────────────────────────────────────── */
.file-list { max-height: 200px; overflow-y: auto; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px; margin-top: 10px; }
.file-item { display: flex; align-items: center; padding: 5px 10px; border-bottom: 1px solid #f0f0f0; }
.file-item:last-child { border-bottom: none; }
.file-item i { margin-right: 10px; color: #0d6efd; }
.file-item .file-name { flex: 1; font-size: 0.9rem; }
.file-item .file-size { color: #6c757d; font-size: 0.8rem; margin-right: 10px; }
.file-item .remove-file { color: #dc3545; cursor: pointer; transition: all 0.3s; }
.file-item .remove-file:hover { transform: scale(1.2); }

/* ── Bildirim uyarıları ─────────────────────────────────────────── */
.notification-alert { animation: slideIn 0.3s ease-out; z-index: 9999; }
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to   { transform: translateX(0);    opacity: 1; }
}

/* ── İstatistik kartları ────────────────────────────────────────── */
.stat-card { transition: all 0.3s; }
.stat-card:hover { transform: scale(1.05); }

/* ── Domain rozeti ──────────────────────────────────────────────── */
.domain-badge { background-color: #e9ecef; color: #495057; padding: 3px 8px; border-radius: 15px; font-size: 0.75rem; }

/* ── Çoklu dosya sayaç rozeti ───────────────────────────────────── */
.multi-file-badge { background-color: #28a745; color: white; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; margin-left: 10px; }
""",

    # ══════════════════════════════════════════════════════════════
    # static/js/script.js  –  Saf JavaScript (jQuery gereksiz)
    # ══════════════════════════════════════════════════════════════
    'static/js/script.js': """/**
 * static/js/script.js
 * ────────────────────
 * Email & URL Scraper – İstemci tarafı JavaScript
 * jQuery bağımlılığı yoktur; modern tarayıcı API'leri kullanılır.
 *
 * İçerik:
 *   • Bootstrap tooltip başlatma
 *   • Tekli ve çoklu dosya yükleme alanı yönetimi
 *   • Drag & drop dosya sürükleme
 *   • Kaydırma butonları (scroll top/bottom)
 *   • Form doğrulama
 *   • Bildirim uyarıları
 */

// ── Sayfa yüklenince tüm modülleri başlat ──────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    initializeTooltips();       // Bootstrap tooltip'lerini etkinleştir
    initializeFileUpload();     // Tekli dosya yükleme alanları
    initializeMultiFileUpload(); // Çoklu dosya yükleme alanları
    updateTimestamp();          // [data-timestamp] öğelerini güncelle
    setupScrollButton();        // Kaydırma butonlarını etkinleştir
    setupFormValidation();      // Form gönderimlerini doğrula
    setupDragAndDrop();         // Sürükle-bırak dosya yükleme
});


// ── Bootstrap tooltip başlatma ──────────────────────────────────────
function initializeTooltips() {
    // data-bs-toggle="tooltip" özelliğine sahip tüm öğeleri bul ve başlat
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
    });
}


// ── Tekli dosya yükleme alanı ───────────────────────────────────────
function initializeFileUpload() {
    // Çoklu seçim olmayan dosya input'larını bul
    document.querySelectorAll('input[type="file"]:not([multiple])').forEach(input => {
        input.addEventListener('change', function () {
            // Yanındaki .file-name etiketini dosya adıyla güncelle
            const label = this.nextElementSibling;
            if (label && label.classList.contains('file-name')) {
                label.textContent = this.files.length > 0
                    ? this.files[0].name
                    : 'Dosya seçilmedi';
            }
        });
    });
}


// ── Çoklu dosya yükleme alanı ───────────────────────────────────────
function initializeMultiFileUpload() {
    // multiple özellikli tüm dosya input'larını bul
    document.querySelectorAll('input[type="file"][multiple]').forEach(input => {
        // Dosya listesini göstermek için container oluştur
        const container = document.createElement('div');
        container.className = 'file-list mt-2';
        input.parentNode.insertBefore(container, input.nextSibling);

        // Kaç dosya seçildiğini gösteren rozet oluştur
        const counter = document.createElement('span');
        counter.className = 'multi-file-badge badge bg-success';
        counter.style.display = 'none'; // Başlangıçta gizli
        input.parentNode.insertBefore(counter, input.nextSibling);

        // Dosya seçimi değiştiğinde listeyi güncelle
        input.addEventListener('change', () => updateFileList(input, container, counter));
    });
}


// ── Seçilen dosya listesini DOM'da güncelle ─────────────────────────
function updateFileList(input, container, counter) {
    const files = Array.from(input.files);

    if (!files.length) {
        container.innerHTML = '';
        counter.style.display = 'none';
        return;
    }

    // Rozeti güncelle
    counter.textContent = files.length + ' dosya seçildi';
    counter.style.display = 'inline-block';

    // Liste başlığı ve temizle butonu
    let html = '<div class="file-list-header d-flex justify-content-between align-items-center mb-2">'
             + '<small class="text-muted">Seçilen dosyalar:</small>'
             + '<button type="button" class="btn btn-sm btn-link text-danger clear-files">Temizle</button>'
             + '</div>';

    // Her dosya için bir satır oluştur
    files.forEach((file, i) => {
        html += `<div class="file-item" data-index="${i}">
            <i class="bi bi-file-earmark"></i>
            <span class="file-name">${file.name}</span>
            <span class="file-size">${formatFileSize(file.size)}</span>
            <i class="bi bi-x-circle remove-file" data-index="${i}"></i>
        </div>`;
    });
    container.innerHTML = html;

    // "Temizle" butonuna tıklanınca tüm seçimi sıfırla
    container.querySelector('.clear-files')?.addEventListener('click', () => {
        input.value = '';
        container.innerHTML = '';
        counter.style.display = 'none';
    });

    // Tek dosya kaldırma butonlarına olay dinleyici ekle
    container.querySelectorAll('.remove-file').forEach(btn => {
        btn.addEventListener('click', function () {
            removeFileFromInput(input, parseInt(this.dataset.index), container, counter);
        });
    });
}


// ── Tek dosyayı seçimden kaldır ─────────────────────────────────────
function removeFileFromInput(input, index, container, counter) {
    // DataTransfer ile yeni dosya listesi oluştur (kaldırılan hariç)
    const dt = new DataTransfer();
    Array.from(input.files).forEach((f, i) => {
        if (i !== index) dt.items.add(f);  // Seçilen index'i atla
    });
    input.files = dt.files;  // Input'u güncelle
    updateFileList(input, container, counter); // Listeyi yeniden render et
}


// ── Dosya boyutunu okunabilir formata çevir ─────────────────────────
function formatFileSize(bytes) {
    if (!bytes) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}


// ── Drag & Drop dosya sürükleme ─────────────────────────────────────
function setupDragAndDrop() {
    document.querySelectorAll('.file-upload').forEach(zone => {
        // Tüm drag event'lerinde varsayılan tarayıcı davranışını engelle
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(ev =>
            zone.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); }, false)
        );

        // Dosya üzerine gelince yeşil kenarlık göster
        ['dragenter', 'dragover'].forEach(ev =>
            zone.addEventListener(ev, () => zone.classList.add('dragover'))
        );

        // Dosya ayrılınca veya bırakılınca kenarlığı kaldır
        ['dragleave', 'drop'].forEach(ev =>
            zone.addEventListener(ev, () => zone.classList.remove('dragover'))
        );

        // Dosya bırakıldığında input'a ekle
        zone.addEventListener('drop', e => {
            const fileInput = zone.querySelector('input[type="file"]');
            if (!fileInput) return;

            // Mevcut dosyaları koru, yeni dosyaları ekle
            const dt = new DataTransfer();
            if (fileInput.multiple) {
                Array.from(fileInput.files).forEach(f => dt.items.add(f));
            }
            Array.from(e.dataTransfer.files).forEach(f => dt.items.add(f));
            fileInput.files = dt.files;

            // Change event'ini manuel tetikle (dinleyiciler devreye girsin)
            fileInput.dispatchEvent(new Event('change', { bubbles: true }));
        });
    });
}


// ── Zaman damgası güncelleme ────────────────────────────────────────
function updateTimestamp() {
    // [data-timestamp] özelliğine sahip öğeleri şu anki saat ile doldur
    document.querySelectorAll('[data-timestamp]').forEach(el => {
        el.textContent = new Date().toLocaleString('tr-TR');
    });
}


// ── Kaydırma butonları ──────────────────────────────────────────────
function setupScrollButton() {
    const topBtn = document.getElementById('scrollTopBtn');
    const botBtn = document.getElementById('scrollBottomBtn');

    function updateBtns() {
        // 300px'den fazla kaydırıldıysa "yukarı" butonu göster
        const scrolled  = window.scrollY > 300;
        // Sayfa sonuna gelinmişse "aşağı" butonu gizle
        const atBottom  = (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50;
        if (topBtn) topBtn.style.display = scrolled   ? 'block' : 'none';
        if (botBtn) botBtn.style.display = atBottom   ? 'none'  : 'block';
    }

    window.addEventListener('scroll', updateBtns);
    updateBtns(); // Sayfa yüklenince ilk durumu ayarla
}

/** Sayfanın en üstüne kaydır */
function scrollToTop()    { window.scrollTo({ top: 0,                         behavior: 'smooth' }); }

/** Sayfanın en altına kaydır */
function scrollToBottom() { window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }); }


// ── Form doğrulama ──────────────────────────────────────────────────
function setupFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (e) {
            const urlInput   = this.querySelector('input[type="url"]');
            const fileInputs = this.querySelectorAll('input[type="file"]');
            const hasFile    = Array.from(fileInputs).some(i => i.files.length > 0);

            // URL alanı varsa ve boşsa gönderimi engelle
            if (urlInput && !urlInput.value.trim()) {
                e.preventDefault();
                showNotification('Lütfen bir URL girin!', 'warning');
                return;
            }

            // Dosya alanı varsa ama dosya seçilmemişse gönderimi engelle
            if (fileInputs.length > 0 && !hasFile) {
                e.preventDefault();
                showNotification('Lütfen en az bir dosya seçin!', 'warning');
            }
        });
    });
}


// ── Bildirim uyarısı göster ─────────────────────────────────────────
/**
 * Ekranın sağ üst köşesinde geçici bir Bootstrap uyarısı gösterir.
 * 3 saniye sonra otomatik olarak kaybolur.
 *
 * @param {string} message - Gösterilecek mesaj
 * @param {string} type    - Bootstrap renk sınıfı: 'info', 'warning', 'danger', 'success'
 */
function showNotification(message, type = 'info') {
    document.querySelector('.notification-alert')?.remove(); // Varsa eskiyi kaldır

    const alert = document.createElement('div');
    alert.className = `notification-alert alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alert.style.zIndex = '9999';
    alert.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.appendChild(alert);

    // 3 saniye sonra otomatik kaldır
    setTimeout(() => alert.parentNode && alert.remove(), 3000);
}


// ── Örnek URL doldurma ──────────────────────────────────────────────
/**
 * Sayfa üzerindeki 'url_input' alanına örnek bir URL yazar.
 * HTML'de 'onclick="setExampleUrl(\'https://...\'')" şeklinde çağrılır.
 *
 * @param {string} url - Doldurulacak URL
 */
function setExampleUrl(url) {
    const el = document.getElementById('url_input');
    if (el) el.value = url;
}
""",
}

# ────────────────────────────────────────────────────────────────────────────────
# DOSYA OLUŞTURMA
# Her dosya yolunu ve içeriğini diske yaz
# ────────────────────────────────────────────────────────────────────────────────
for path, content in files.items():
    # Dosyanın bulunduğu klasörü oluştur (alt klasörler için de gerekli)
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Dosyayı UTF-8 ile yaz
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ────────────────────────────────────────────────────────────────────────────────
# KURULUM ÖZETI
# ────────────────────────────────────────────────────────────────────────────────
print("✅ Tüm proje dosyaları başarıyla oluşturuldu!")
print()
print("📁 Oluşturulan dosyalar:")
for path in sorted(files.keys()):
    print(f"   {path}")
print()
print("🔒 Güvenlik hatırlatması:")
print("   • .env dosyasındaki SECRET_KEY'i değiştir!")
print("   • .env dosyasını Git'e commit etme (.gitignore'da zaten var)")
print()
print("📦 Kurulum adımları:")
print("   1. pip install -r requirements.txt")
print("   2. .env dosyasındaki SECRET_KEY'i güçlü bir değerle değiştir")
print("   3. python app.py")
print("   4. Tarayıcında aç: http://localhost:5000")
