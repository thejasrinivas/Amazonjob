# 🚀 Amazon Job Agent AI

An automated cloud-based agent that monitors the Amazon Jobs portal for new openings in a specific area. It uses **Playwright** for browser automation, **BeautifulSoup** for data extraction, and **GitHub Actions** to run 24/7 for free.

## 🛠️ Features
* **Cloud Automation:** Runs every 1-5 minutes via GitHub Actions.
* **Smart Stealth:** Bypasses bot detection using custom headers and stealth scripts.
* **Dual Alerts:** Sends instant notifications via **Telegram** and **Email**.
* **Auto-Cleanup:** Automatically handles cookie consents and popups.
* **Zero Maintenance:** No need to keep your PC on; it lives in the cloud.

---

## 📋 Setup Instructions

### 1. External Service Configuration

#### **Telegram Bot (Alerts)**
1. Message [@BotFather](https://t.me/botfather) on Telegram and send `/newbot`.
2. Save the **API Token** provided.
3. Message [@userinfobot](https://t.me/userinfobot) to get your **Chat ID**.
4. Send a `/start` message to your new bot.

#### **Gmail App Password (Email)**
1. Go to your Google Account Settings > Security.
2. Enable **2-Step Verification**.
3. Search for **App Passwords**.
4. Create a new one called "Amazon Bot" and save the 16-character code.

---

### 2. GitHub Secrets Setup
To keep your credentials safe, add these secrets in your repository:
**Settings > Secrets and variables > Actions > New repository secret**

| Secret Name | Description |
| :--- | :--- |
| `PINCODE` | The UK postcode to search (e.g., BL21JA). |
| `TELEGRAM_TOKEN` | The API Token from BotFather. |
| `TELEGRAM_CHAT_ID` | Your numerical User ID. |
| `EMAIL_SENDER` | Your Gmail address. |
| `EMAIL_PASSWORD` | The 16-character App Password. |
| `EMAIL_RECEIVER` | The email address where you want to receive alerts. |

---

## 🏗️ Technical Architecture

### **The Scraper (`amazon.py`)**
The script uses **Playwright** in `headless` mode.
* It injects JavaScript to hide the `navigator.webdriver` property (Stealth).
* It clears overlapping popups using `aria-label` selectors.
* It parses the page content with **BeautifulSoup** to extract job titles and locations from `JobCard` containers.



### **The Workflow (`run_agent.yml`)**
The automation is handled by GitHub Actions.
* **Trigger:** A `cron` schedule runs the script periodically.
* **Environment:** GitHub injects the encrypted Secrets into the script at runtime.
* **Artifacts:** If a run fails, a `debug_view.png` screenshot is saved as a GitHub Artifact so you can see what went wrong.



---

## 📦 Dependencies
Installed via `requirements.txt`:
* `playwright`: Browser automation.
* `beautifulsoup4`: HTML parsing.
* `requests`: Telegram API communication.

---

## 🚦 Usage
1. **Manual Run:** Go to the **Actions** tab, select the workflow, and click **Run workflow**.
2. **Automatic:** The bot will trigger automatically based on the `cron` schedule.
3. **Logs:** View the "Run Scraper" step in the Actions logs to see the bot's live progress.