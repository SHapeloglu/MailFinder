import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def extract_urls_from_text(text):
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s<>"{}|\\^`\[\]]*|www\.[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    json_url_pattern = r'"url"\s*:\s*"([^"]+)"'
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
        return ''