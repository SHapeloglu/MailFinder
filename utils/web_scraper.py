import requests
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
    
    return sorted(all_emails), sorted(all_urls), scraped_pages