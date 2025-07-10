from app.scraper.extractors import extract_data
from app.scraper.dynamic import handle_dynamic
from app.scraper.pagination import handle_pagination
from app.scraper.url_discovery import discover_urls
from app.models import ScrapeTask, ScrapeResult
from app.database import SessionLocal
from loguru import logger
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
import json
import re
import unicodedata

def sanitize_text_for_pdf(text):
    if not text:
        return ""
    
    text = str(text)
    
    unicode_replacements = {
        '\u2013': '-', 
        '\u2014': '--',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2026': '...',
        '\u00a0': ' ',
        '\u00ae': '(R)',
        '\u00a9': '(C)',
        '\u2122': '(TM)',
    }
    
    for unicode_char, ascii_replacement in unicode_replacements.items():
        text = text.replace(unicode_char, ascii_replacement)

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F" 
        "\U0001F300-\U0001F5FF" 
        "\U0001F680-\U0001F6FF"  
        "\U0001F1E0-\U0001F1FF" 
        "\U00002702-\U000027B0" 
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF" 
        "\U0001FA70-\U0001FAFF"
        "]+", 
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    try:
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ascii', 'ignore').decode('ascii')
    except UnicodeError:
        text = ''.join(char for char in text if ord(char) < 256)
    
    text = ' '.join(text.split())
    text = re.sub(r'[^\x20-\x7E]', '', text)
    
    return text

def generate_pdf_report(task_id: int, scraped_data: list) -> str:    
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scraping_report_{task_id}_{timestamp}.pdf"
    pdf_path = reports_dir / filename
    
    try:
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 20)
        header_text = sanitize_text_for_pdf(f'Web Scraping Report - Task {task_id}')
        pdf.cell(0, 15, header_text, ln=True, align='C')
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Executive Summary', ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f'Total Records Extracted: {len(scraped_data)}', ln=True)
        pdf.cell(0, 8, f'Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
        pdf.ln(10)
        
        for i, item in enumerate(scraped_data, 1):
            if pdf.get_y() > 250:
                pdf.add_page()
            
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'Record {i}', ln=True)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(30, 6, 'URL:', 0, 0)
            pdf.set_font('Arial', '', 10)
            url_text = sanitize_text_for_pdf(item.get("url", "N/A"))
            if len(url_text) > 60:
                url_text = url_text[:60] + "..."
            pdf.cell(0, 6, url_text, ln=True)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(30, 6, 'Company:', 0, 0)
            pdf.set_font('Arial', '', 10)
            company_text = sanitize_text_for_pdf(item.get("company", "N/A"))
            pdf.cell(0, 6, company_text, ln=True)
            contacts = item.get("contacts", {})
            if isinstance(contacts, dict):
                emails = contacts.get("emails", [])
                if emails and isinstance(emails, list) and len(emails) > 0:
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(30, 6, 'Emails:', 0, 0)
                    pdf.set_font('Arial', '', 10)
                    email_list = [sanitize_text_for_pdf(str(email)) for email in emails if email]
                    emails_text = ", ".join(email_list[:3])
                    if len(email_list) > 3:
                        emails_text += f" (+{len(email_list)-3} more)"
                    pdf.cell(0, 6, emails_text, ln=True)
                
                phones = contacts.get("phones", [])
                if phones and isinstance(phones, list) and len(phones) > 0:
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(30, 6, 'Phones:', 0, 0)
                    pdf.set_font('Arial', '', 10)
                    phone_list = [sanitize_text_for_pdf(str(phone)) for phone in phones if phone]
                    phones_text = ", ".join(phone_list[:3])
                    if len(phone_list) > 3:
                        phones_text += f" (+{len(phone_list)-3} more)"
                    pdf.cell(0, 6, phones_text, ln=True)
            
            tagline = item.get("tagline")
            if tagline:
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(30, 6, 'Tagline:', 0, 0)
                pdf.set_font('Arial', '', 10)
                tagline_text = sanitize_text_for_pdf(str(tagline))
                if len(tagline_text) > 80:
                    tagline_text = tagline_text[:80] + "..."
                pdf.cell(0, 6, tagline_text, ln=True)
            
            description = item.get("description")
            if description:
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(30, 6, 'Description:', 0, 0)
                pdf.set_font('Arial', '', 10)
                desc_text = sanitize_text_for_pdf(str(description))
                if len(desc_text) > 100:
                    desc_text = desc_text[:100] + "..."
                pdf.cell(0, 6, desc_text, ln=True)
            
            services = item.get("services", [])
            if services and isinstance(services, list) and len(services) > 0:
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(30, 6, 'Services:', 0, 0)
                pdf.set_font('Arial', '', 10)
                service_list = [sanitize_text_for_pdf(str(service)) for service in services if service]
                services_text = ", ".join(service_list[:5])
                if len(service_list) > 5:
                    services_text += f" (+{len(service_list)-5} more)"
                pdf.cell(0, 6, services_text, ln=True)
            
            social_media = item.get("social_media", {})
            if social_media and isinstance(social_media, dict):
                social_links = []
                for platform, link in social_media.items():
                    if link:
                        clean_platform = sanitize_text_for_pdf(str(platform))
                        social_links.append(clean_platform)
                
                if social_links:
                    pdf.set_font('Arial', 'B', 10)
                    pdf.cell(30, 6, 'Social:', 0, 0)
                    pdf.set_font('Arial', '', 10)
                    social_text = ", ".join(social_links[:3])
                    if len(social_links) > 3:
                        social_text += f" (+{len(social_links)-3} more)"
                    pdf.cell(0, 6, social_text, ln=True)
            
            industry = item.get("industry")
            if industry:
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(30, 6, 'Industry:', 0, 0)
                pdf.set_font('Arial', '', 10)
                industry_text = sanitize_text_for_pdf(str(industry))
                pdf.cell(0, 6, industry_text, ln=True)
            
            pdf.ln(5)
        
        pdf.output(str(pdf_path))
        logger.info(f"PDF report generated successfully: {pdf_path}")
        return str(pdf_path)
        
    except Exception as e:
        logger.error(f"Failed to generate PDF for task {task_id}: {str(e)}")
        raise e

def run_scraper(task_id, params):
    db = SessionLocal()
    task = None
    final_status = "failed"
    
    try:
        task = db.query(ScrapeTask).filter(ScrapeTask.id == task_id).first()
        if not task:
            logger.error(f"Task {task_id} not found")
            return
            
        task.status = "running"
        db.commit()
        logger.info(f"Starting scraping task {task_id} for URL: {params['url']}")
        
        successful_extractions = 0
        failed_extractions = 0
        all_data = []
        
        try:
            urls = discover_urls(params["url"])
            logger.info(f"Discovered {len(urls)} URLs to scrape for task {task_id}")
        except Exception as e:
            logger.error(f"URL discovery failed for task {task_id}: {str(e)}")
            urls = [params["url"]]
        
        for url_index, url in enumerate(urls, 1):
            try:
                logger.info(f"Processing URL {url_index}/{len(urls)}: {url}")
                
                try:
                    html = handle_dynamic(url)
                    logger.debug(f"Successfully loaded dynamic content for {url}")
                except Exception as e:
                    logger.warning(f"Dynamic content loading failed for {url}: {str(e)}")
                    import requests
                    try:
                        response = requests.get(url, timeout=10, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        })
                        html = response.text
                    except Exception as req_e:
                        logger.error(f"Requests fallback also failed for {url}: {str(req_e)}")
                        failed_extractions += 1
                        continue
                
                try:
                    paginated_htmls = handle_pagination(html, url)
                    logger.debug(f"Found {len(paginated_htmls)} pages for {url}")
                except Exception as e:
                    logger.warning(f"Pagination handling failed for {url}: {str(e)}")
                    paginated_htmls = [html] 
                
                for page_index, page_html in enumerate(paginated_htmls, 1):
                    try:
                        data = extract_data(page_html, url)
                        
                        if data and any(data.values()):
                            # Add metadata
                            data["extracted_at"] = datetime.now().isoformat()
                            data["page_number"] = page_index
                            data["task_id"] = task_id
                            
                            all_data.append(data)
                            successful_extractions += 1
                            logger.info(f"Successfully extracted data from {url} (page {page_index})")
                        else:
                            logger.warning(f"No meaningful data extracted from {url} (page {page_index})")
                            failed_extractions += 1
                            
                    except Exception as e:
                        logger.error(f"Data extraction failed for {url} (page {page_index}): {str(e)}")
                        failed_extractions += 1
                        continue
                        
            except Exception as e:
                logger.error(f"Failed to process URL {url}: {str(e)}")
                failed_extractions += 1
                continue
        
        logger.info(f"Scraping completed. Successful: {successful_extractions}, Failed: {failed_extractions}")
        
        if all_data:
            try:
                result = ScrapeResult(task_id=task_id, data=all_data)
                db.add(result)
                db.commit()
                logger.info(f"Successfully saved {len(all_data)} records for task {task_id}")
                try:
                    logger.info(f"Generating PDF report for task {task_id}")
                    pdf_path = generate_pdf_report(task_id, all_data)
                    logger.info(f"PDF report generated successfully: {pdf_path}")
                    task.pdf_path = pdf_path
                    task.status = "completed"
                    final_status = "completed"
                    db.commit()
                    
                except Exception as e:
                    logger.error(f"PDF generation failed for task {task_id}: {str(e)}")
                    task.status = "completed"
                    final_status = "completed"
                    db.commit()
                
            except Exception as e:
                logger.error(f"Failed to save results for task {task_id}: {str(e)}")
                task.status = "failed"
                final_status = "failed"
                db.commit()
                
        else:
            logger.warning(f"No data extracted for task {task_id}")
            task.status = "failed"
            final_status = "failed"
            db.commit()
            
    except Exception as e:
        logger.error(f"Critical error in scraping task {task_id}: {str(e)}")
        try:
            if task:
                task.status = "failed"
                final_status = "failed"
                db.commit()
        except Exception as db_e:
            logger.error(f"Failed to update task status: {str(db_e)}")
                
    finally:
        logger.info(f"Scraping task {task_id} completed with status: {final_status}")
        try:
            db.close()
        except Exception as close_e:
            logger.error(f"Error closing database connection: {str(close_e)}")
