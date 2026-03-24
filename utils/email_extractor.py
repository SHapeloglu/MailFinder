import re
from bs4 import BeautifulSoup

def extract_emails_from_text(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    json_email_pattern = r'"email"\s*:\s*"([^"]+)"'
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
    return sorted(all_emails)