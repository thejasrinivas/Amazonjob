import os
import time
import smtplib
import requests
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# --- CONFIG ---
PINCODE = " "
URL = "https://www.jobsatamazon.co.uk/app#/jobSearch"

# --- TELEGRAM CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_telegram_alert(message):
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    tg_payload = {"chat_id": TELEGRAM_CHAT_ID, "text": job_summary, "parse_mode": "HTML"}
    requests.post(tg_url, data=tg_payload)


def send_email(job_details):
    msg = MIMEText(job_summary, 'html')
    msg['Subject'] = f"🚨 Amazon Job Alert: {PINCODE}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        
def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            page.goto(URL, wait_until="load")
            # --- POPUP CLEANUP (Using your screenshot info) ---
            # 1. Close Cookie/Consent Popup
            try:
                page.wait_for_selector('button[aria-label*="Close cookie consent"]', timeout=5000)
                page.click('button[aria-label*="Close cookie consent"]')
            except: pass

            # 2. Close "Want to get notified" (The second 'X' you saw)
            try:
                page.wait_for_selector('button[aria-label="Close"]', timeout=3000)
                page.click('button[aria-label="Close"]')
            except: pass

            # --- SEARCH PHASE ---
            print("Entering Pincode...")
            page.wait_for_selector('#zipcode-nav-search', timeout=10000)
            page.fill('#zipcode-nav-search', PINCODE)
            page.keyboard.press("Enter")
            
            # Allow time for results to render
            time.sleep(7) 
            
            # Parse results
            soup = BeautifulSoup(page.content(), 'html.parser')
            jobs = soup.find_all('div', {'data-test-id': 'JobCard'})
            
            if jobs:
                print(f"🔥 Found {len(jobs)} jobs! Checking email...")
                job_summary = f"<b>🔥 {len(jobs)} AMAZON JOBS FOUND!</b>\n\n"
                for job in jobs:
                    title = job.find('strong').text.strip() if job.find('strong') else "Warehouse Role"
                    loc_divs = job.find_all('div', class_='jobDetailText')
                    location = loc_divs[-1].text.strip() if loc_divs else "Unknown Location"
                    job_summary += f"📍 {title}\n🏢 {location}\n\n"
                
                job_summary += f'<a href="{URL}">Apply Here</a>'
                
                # Send both Email AND Telegram for safety
                send_email(job_summary)
                send_telegram_alert(job_summary)
            else:
                print("😴 No jobs yet.")

        except Exception as e:
            print(f"⚠️ Agent encountered an issue: {e}")
            page.screenshot(path="debug_view.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run_scraper()