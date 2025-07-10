from bs4 import BeautifulSoup
import requests

def handle_pagination(html, base_url):
    pages = [html]
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.find("a", text=lambda t: t and "next" in t.lower())
    while next_link:
        next_url = next_link.get("href")
        if not next_url.startswith("http"):
            next_url = base_url.rstrip("/") + "/" + next_url.lstrip("/")
        resp = requests.get(next_url)
        if resp.status_code != 200:
            break
        pages.append(resp.text)
        soup = BeautifulSoup(resp.text, "html.parser")
        next_link = soup.find("a", text=lambda t: t and "next" in t.lower())
    return pages