
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
from typing import List, Dict, Optional, Set

class EnhancedDataExtractor:
    def __init__(self):
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )

        self.phone_patterns = [
            re.compile(r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'),  # US format
            re.compile(r'\+?[0-9]{1,4}[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}'),  # General
            re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'),  # Simple US
            re.compile(r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}')  # (123) 456-7890
        ]

        self.social_patterns = {
            'linkedin': re.compile(r'linkedin\.com/(?:in|company)/([^/\s]+)', re.IGNORECASE),
            'twitter': re.compile(r'twitter\.com/([^/\s]+)', re.IGNORECASE),
            'facebook': re.compile(r'facebook\.com/([^/\s]+)', re.IGNORECASE),
            'instagram': re.compile(r'instagram\.com/([^/\s]+)', re.IGNORECASE)
        }

def extract_data(html: str, url: str) -> Dict:
    extractor = EnhancedDataExtractor()
    soup = BeautifulSoup(html, "html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text()

    return {
        "url": url,
        "company": _extract_company_info(soup, text),
        "contacts": _extract_contact_info(soup, text, extractor),
        "tagline": _extract_tagline(soup, text),
        "services": _extract_services(soup, text),
        "social_media": _extract_social_media(soup, text, extractor),
        "address": _extract_address(soup, text),
        "description": _extract_description(soup, text),
        "industry": _extract_industry(soup, text)
    }

def _extract_company_info(soup: BeautifulSoup, text: str) -> Optional[str]:
    company_selectors = [
        'h1', '.company-name', '.org-title', '.company-title',
        '[data-testid*="company"]', '.business-name', '.brand-name',
        '.site-title', '.logo-text', 'title', '.header-title',
        '.hero-title', '.main-title', '[class*="company"]',
        '[class*="brand"]', '[id*="company"]'
    ]

    for selector in company_selectors:
        element = soup.select_one(selector)
        if element and element.text.strip():
            company_name = element.text.strip()
            if len(company_name) > 2 and len(company_name) < 100:
                return company_name

    meta_company = soup.select_one('meta[property="og:site_name"]')
    if meta_company:
        return meta_company.get('content', '').strip()

    title_tag = soup.select_one('title')
    if title_tag:
        title_text = title_tag.text.strip()
        for separator in [' | ', ' - ', ' – ', ' :: ']:
            if separator in title_text:
                return title_text.split(separator)[0].strip()

    return None

def _extract_contact_info(soup: BeautifulSoup, text: str, extractor: EnhancedDataExtractor) -> Dict:
    contacts = {
        'emails': _extract_emails(soup, text, extractor),
        'phones': _extract_phones(soup, text, extractor),
        'contact_page': _find_contact_page_url(soup)
    }
    return contacts

def _extract_emails(soup: BeautifulSoup, text: str, extractor: EnhancedDataExtractor) -> List[str]:
    emails = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('mailto:'):
            email = href.replace('mailto:', '').split('?')[0]
            emails.add(email)

    text_emails = extractor.email_pattern.findall(text)
    emails.update(text_emails)

    valid_emails = []
    for email in emails:
        if '@' in email and '.' in email.split('@')[1]:
            if not any(placeholder in email.lower() for placeholder in 
                      ['example', 'test', 'dummy', 'placeholder', 'yourname']):
                valid_emails.append(email)

    return list(set(valid_emails))

def _extract_phones(soup: BeautifulSoup, text: str, extractor: EnhancedDataExtractor) -> List[str]:
    phones = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('tel:'):
            phone = href.replace('tel:', '')
            phones.add(phone)

    for pattern in extractor.phone_patterns:
        matches = pattern.findall(text)
        for match in matches:
            if isinstance(match, tuple):
                phone = ''.join(match)
            else:
                phone = match
            phones.add(phone)

    valid_phones = []
    for phone in phones:
        try:
            cleaned = re.sub(r'[^\d+]', '', phone)
            if len(cleaned) >= 10 and len(cleaned) <= 15:
                valid_phones.append(phone)
        except:
            continue

    return list(set(valid_phones))

def _find_contact_page_url(soup: BeautifulSoup) -> Optional[str]:
    contact_keywords = ['contact', 'about', 'reach', 'connect', 'get in touch']

    for link in soup.find_all('a', href=True):
        link_text = link.text.lower().strip()
        href = link['href']

        if any(keyword in link_text for keyword in contact_keywords):
            return href

    return None

def _extract_tagline(soup: BeautifulSoup, text: str) -> Optional[str]:
    tagline_selectors = [
        '.tagline', '.slogan', '.subtitle', '.hero-subtitle',
        '.lead', '.description', '.intro', 'p.lead',
        '.hero-description', '[class*="tagline"]', '[class*="slogan"]',
        'meta[name="description"]', 'meta[property="og:description"]'
    ]

    for selector in tagline_selectors:
        if selector.startswith('meta'):
            element = soup.select_one(selector)
            if element:
                content = element.get('content', '').strip()
                if 20 <= len(content) <= 200:
                    return content
        else:
            element = soup.select_one(selector)
            if element and element.text.strip():
                tagline = element.text.strip()
                if 10 <= len(tagline) <= 200:
                    return tagline

    paragraphs = soup.find_all('p')
    for p in paragraphs[:3]:
        text = p.text.strip()
        if 20 <= len(text) <= 150 and not text.startswith(('The', 'This', 'Our')):
            return text

    return None

def _extract_services(soup: BeautifulSoup, text: str) -> List[str]:
    services = set()

    service_selectors = [
        '.services li', '.offerings li', '.products li',
        '.features li', '[class*="service"] li', '[class*="product"] li',
        '.what-we-do li', '.our-services li', '.capabilities li'
    ]

    for selector in service_selectors:
        elements = soup.select(selector)
        for element in elements:
            service_text = element.text.strip()
            if 3 <= len(service_text) <= 100:
                services.add(service_text)

    headers = soup.find_all(['h2', 'h3', 'h4'])
    for header in headers:
        text = header.text.strip().lower()
        if any(keyword in text for keyword in ['service', 'offering', 'product', 'solution']):
            next_elem = header.find_next_sibling(['ul', 'ol', 'div'])
            if next_elem:
                items = next_elem.find_all('li') or next_elem.find_all('p')
                for item in items[:5]:
                    service_text = item.text.strip()
                    if 3 <= len(service_text) <= 100:
                        services.add(service_text)

    return list(services)[:10]

def _extract_social_media(soup: BeautifulSoup, text: str, extractor: EnhancedDataExtractor) -> Dict[str, str]:
    social_media = {}

    for link in soup.find_all('a', href=True):
        href = link['href']
        for platform, pattern in extractor.social_patterns.items():
            match = pattern.search(href)
            if match:
                social_media[platform] = href
                break

    return social_media

def _extract_address(soup: BeautifulSoup, text: str) -> Optional[str]:
    address_selectors = [
        '.address', '.location', '.contact-address',
        '[itemtype*="PostalAddress"]', '.postal-address',
        '[class*="address"]', '[class*="location"]'
    ]

    for selector in address_selectors:
        element = soup.select_one(selector)
        if element:
            address_text = element.text.strip()
            if len(address_text) > 10:
                return address_text

    address_pattern = re.compile(r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Road|Nagar|Rasta|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl)(?:,\s*[A-Za-z\s]+)*,\s*[A-Z]{2}\s+\d{5}', re.IGNORECASE)
    match = address_pattern.search(text)
    if match:
        return match.group(0)

    return None

def _extract_description(soup: BeautifulSoup, text: str) -> Optional[str]:
    meta_desc = soup.select_one('meta[name="description"]')
    if meta_desc:
        desc = meta_desc.get('content', '').strip()
        if 50 <= len(desc) <= 500:
            return desc

    about_headers = soup.find_all(['h1', 'h2', 'h3'], string=re.compile(r'about|who we are|our story', re.IGNORECASE))
    for header in about_headers:
        next_elem = header.find_next(['p', 'div'])
        if next_elem:
            desc = next_elem.text.strip()
            if 50 <= len(desc) <= 500:
                return desc

    return None

def _extract_industry(soup: BeautifulSoup, text: str) -> Optional[str]:
    industries = [
        'technology', 'healthcare', 'finance', 'education', 'retail',
        'manufacturing', 'consulting', 'marketing', 'real estate',
        'construction', 'automotive', 'food', 'travel', 'entertainment',
        'software', 'hardware', 'services', 'e-commerce', 'nonprofit'
    ]

    text_lower = text.lower()
    for industry in industries:
        if industry in text_lower:
            return industry.title()

    return None
