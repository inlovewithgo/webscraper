import requests
from bs4 import BeautifulSoup

def discover_urls(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    return [url] + [l for l in links if l.startswith("http")]
