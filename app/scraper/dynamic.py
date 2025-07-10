import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging

logger = logging.getLogger(__name__)

def handle_dynamic(url):
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        if response.status_code == 200:
            logger.info(f"Successfully got content with requests for {url}")
            return response.text
    except Exception as e:
        logger.warning(f"Requests failed for {url}: {e}, trying Selenium")
    
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        driver.quit()
        logger.info(f"Successfully got content with Selenium for {url}")
        return html
    except Exception as e:
        logger.error(f"Selenium failed for {url}: {e}")
        return f"<html><body>Error loading {url}: {str(e)}</body></html>"