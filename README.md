# 📧 Email & URL Scraper

> Web sitelerinden ve dosyalardan e-posta adresleri ile URL'leri toplamak, dönüştürmek ve dışa aktarmak için geliştirilmiş Flask tabanlı web uygulaması.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![License](https://img.shields.io/badge/Lisans-MIT-green)

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Modüller](#-modüller)
- [API Rotaları](#-api-rotaları)
- [Güvenlik](#-güvenlik)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## ✨ Özellikler

### 🔍 E-posta & URL Çıkarma
- Web sitesi URL'sinden otomatik e-posta ve URL çıkarma
- Derin tarama modu (alt sayfaları da dahil eder)
- TXT, HTML, CSV, JSON dosyalarından toplu çıkarma
- HTML kaynak kodunu yerel olarak kaydetme

### 📄 Sayfalı Site Tarayıcı
- `?page=1`, `?page=2` gibi sayfalı yapıdaki siteleri otomatik tarar
- Başlangıç / bitiş sayfa aralığı belirleme
- Sayfalar arası gecikme ayarı (bot engellerine karşı)
- Her sayfa için ayrı istatistik

### 🔄 URL → E-posta Dönüştürücü
- TXT/HTML/CSV dosyalarındaki URL'lerden `info@domain.com` formatında e-posta üretir
- 5 öncelik seviyesine göre akıllı dönüşüm
- Toplu dosya işleme

### 🔄 E-posta → URL Dönüştürücü
- E-posta adresinden `https://www.domain.com` URL'si üretir
- Üç farklı URL formatı: `https://www.`, `https://`, `http://www.`
- Metin girişi veya dosya yükleme ile çalışır

### 📊 Excel E-posta Birleştirici
- Birden fazla Excel (`.xlsx`, `.xls`) veya CSV dosyasını birleştirir
- Tüm sütunlardaki e-posta adreslerini otomatik bulur
- Domain bazlı istatistikler
- Tekrar eden adresleri otomatik temizler

### 📥 Çoklu Dışa Aktarma Formatları
| Format | Açıklama |
|--------|----------|
| TXT    | Satır satır liste |
| CSV    | Excel ile uyumlu, UTF-8 BOM |
| XLSX   | Excel formatı |
| JSON   | Makine tarafından okunabilir |

---

## 🖥️ Ekran Görüntüleri

> *(Ekran görüntülerini `docs/screenshots/` klasörüne ekleyip buraya referans verebilirsiniz.)*

---

## 🚀 Kurulum

### Gereksinimler

- Python **3.10+**
- pip

### 1. Depoyu klonla

```bash
git clone https://github.com/kullanici-adi/email-url-scraper.git
cd email-url-scraper
```

### 2. Sanal ortam oluştur (önerilir)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 4. Ortam değişkenlerini yapılandır

```bash
cp .env.example .env
```

`.env` dosyasını düzenle:

```env
SECRET_KEY=buraya-guclu-rastgele-bir-anahtar-yaz
FLASK_ENV=development
MAX_UPLOAD_MB=50
```

> ⚠️ `.env` dosyasını asla Git'e commit etme! `.gitignore`'a ekli olduğundan emin ol.

### 5. Uygulamayı başlat

```bash
python app.py
```

Tarayıcında aç: **http://localhost:5000**

---

## 📖 Kullanım

Detaylı kullanım kılavuzu için [`USAGE.md`](USAGE.md) dosyasına bakın.

### Hızlı Başlangıç

```python
# Projeyi doğrudan proje_olustur.py ile de kurabilirsin:
python proje_olustur.py
# Bu komut tüm klasör yapısını ve dosyaları otomatik oluşturur.
```

---

## 📁 Proje Yapısı

```
email-url-scraper/
│
├── app.py                      # Ana Flask uygulaması, tüm rotalar
├── proje_olustur.py            # Projeyi sıfırdan oluşturan kurulum betiği
├── requirements.txt            # Python bağımlılıkları
├── .env                        # Ortam değişkenleri (git'e eklenmez)
├── .env.example                # Örnek ortam değişkenleri şablonu
├── .gitignore                  # Git dışı bırakılan dosyalar
├── app.log                     # Uygulama log dosyası (otomatik oluşur)
│
├── utils/                      # Yardımcı modüller
│   ├── __init__.py             # Açık import tanımları
│   ├── email_extractor.py      # E-posta çıkarma mantığı
│   ├── url_extractor.py        # URL çıkarma mantığı
│   ├── web_scraper.py          # Web scraping motoru
│   └── file_utils.py           # Dosya doğrulama & güvenli silme
│
├── templates/                  # Jinja2 HTML şablonları
│   ├── base.html               # Temel şablon (navbar, footer)
│   ├── index.html              # Ana sayfa
│   ├── results.html            # Çıkarma sonuçları
│   ├── paginated_scan.html     # Sayfalı tarayıcı
│   ├── url_to_email_converter.html
│   ├── excel_email_merger.html
│   ├── email_to_url.html
│   └── about.html              # Hakkında
│
├── static/
│   ├── css/style.css           # Özel stiller
│   └── js/script.js            # Saf JavaScript (jQuery yok)
│
├── uploads/                    # Geçici yükleme klasörü (otomatik temizlenir)
└── temp_results/               # Geçici JSON sonuçlar (1 saat sonra temizlenir)
```

---

## 🧩 Modüller

### `utils/email_extractor.py`
E-posta adreslerini düz metinden, HTML içeriğinden ve `mailto:` bağlantılarından çıkarır.

```python
from utils.email_extractor import extract_emails_from_text, extract_emails_from_html

emails = extract_emails_from_text("Bize ulaşın: info@sirket.com")
# → ['info@sirket.com']
```

### `utils/url_extractor.py`
URL'leri metinden ve HTML'den çıkarır. Domain ayrıştırmasını da destekler.

```python
from utils.url_extractor import extract_urls_from_text, extract_domain

urls = extract_urls_from_text("Site: https://www.ornek.com")
domain = extract_domain("https://www.ornek.com")
# → 'ornek.com'
```

### `utils/web_scraper.py`
Web sitelerini (tek sayfa veya çok sayfa) tarar; e-posta ve URL toplar.

```python
from utils.web_scraper import scrape_website, scrape_paginated_website

html, emails, urls = scrape_website("https://ornek.com", max_pages=3)
emails, urls, pages = scrape_paginated_website("https://site.com/liste?page=1", 1, 10)
```

### `utils/file_utils.py`
Yüklenen dosyaların uzantı doğrulamasını ve geçici dosyaların güvenli silinmesini yönetir.

```python
from utils.file_utils import allowed_file, safe_delete_upload

allowed_file("veri.csv")    # → True
allowed_file("script.exe")  # → False
safe_delete_upload("/tmp/gecici.txt")
```

---

## 🌐 API Rotaları

| Metot | Rota | Açıklama |
|-------|------|----------|
| GET   | `/` | Ana sayfa |
| POST  | `/extract` | URL veya dosyadan e-posta/URL çıkar |
| GET/POST | `/paginated-scan` | Sayfalı site tarayıcı |
| GET/POST | `/url-to-email` | URL → e-posta dönüştürücü |
| POST  | `/convert-urls` | URL dosyasını işle |
| GET/POST | `/email-to-url` | E-posta → URL dönüştürücü |
| POST  | `/convert-emails-to-urls` | E-posta dosyasını işle |
| GET/POST | `/excel-email-merger` | Excel birleştirici |
| POST  | `/merge-excel-emails` | Excel dosyalarını işle |
| POST  | `/download` | Sonuçları indir (TXT/CSV/JSON) |
| POST  | `/download-converted` | Dönüştürülmüş veriyi indir |
| POST  | `/download-e2u` | E-posta→URL sonuçlarını indir |
| GET   | `/about` | Hakkında sayfası |

---

## 🔒 Güvenlik

Bu uygulama aşağıdaki güvenlik önlemlerini içerir:

| Önlem | Açıklama |
|-------|----------|
| `.env` tabanlı secret key | `SECRET_KEY` asla kaynak kodda saklanmaz |
| Otomatik dosya silme | Yüklenen dosyalar işlem sonrası `safe_delete_upload()` ile silinir |
| Path traversal koruması | `result_key` parametresi UUID regex ile doğrulanır |
| Dosya tipi kısıtlaması | Yalnızca `txt, html, htm, csv, json, xlsx, xls` uzantılarına izin verilir |
| Kullanıcı dostu hata mesajları | Ham exception metni kullanıcıya gösterilmez, loglanır |
| Rate limiting (soft) | Sayfalı taramada maks. 100 sayfa ve min. 0.5 sn gecikme zorunludur |
| Structured logging | Tüm hatalar `app.log` dosyasına kaydedilir |

### Önerilen Ek Önlemler (Production)

```python
# Flask-Limiter ile rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per hour"])

# HTTPS zorunluluğu (nginx veya Gunicorn ile)
# python-magic ile MIME type doğrulaması
```

---

## 🧪 Test

```bash
# Bağımlılıkları kontrol et
python -m pytest tests/ -v

# Manuel test
python -c "from utils.email_extractor import extract_emails_from_text; print(extract_emails_from_text('test@ornek.com'))"
```

---

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni branch oluşturun: `git checkout -b ozellik/yeni-ozellik`
3. Değişikliklerinizi commit edin: `git commit -m 'feat: yeni özellik eklendi'`
4. Branch'inizi push edin: `git push origin ozellik/yeni-ozellik`
5. Pull Request açın

### Commit Mesaj Formatı

```
feat: yeni özellik
fix: hata düzeltmesi
docs: dokümantasyon güncellemesi
refactor: kod yeniden düzenleme
security: güvenlik düzeltmesi
```

---

## 📝 Değişiklik Günlüğü

### v2.1 (Güncel)
- ✅ SECRET_KEY `.env` dosyasına taşındı
- ✅ Upload sonrası otomatik dosya silme
- ✅ Path traversal koruması eklendi
- ✅ `logging` modülü entegre edildi
- ✅ `save_html` özelliği düzeltildi
- ✅ `should_visit()` closure hatası giderildi
- ✅ jQuery bağımlılığı kaldırıldı
- ✅ Wildcard import'lar temizlendi
- ✅ `temp_results/` klasörü artık otomatik oluşturuluyor

### v2.0
- 7 farklı Python betiği tek çatı altında birleştirildi
- Sayfalı tarayıcı eklendi
- Çoklu dosya yükleme desteği
- Excel/CSV birleştirici eklendi

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

## 👤 İletişim

Sorularınız için bir [Issue](../../issues) açabilirsiniz.

---

<p align="center">
  <strong>Email & URL Scraper</strong> — Flask ile geliştirildi 🐍
</p>
