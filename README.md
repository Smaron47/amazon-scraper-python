**Amazon Product Data Scraper**

---

## 1. Project Overview

A Python-based web scraping tool that automates extraction of product information from Amazon India (amazon.in) using Selenium WebDriver. The script reads a list of ASINs (Amazon Standard Identification Numbers) from `urls.txt`, navigates to each product page, and collects:

* **Title**
* **Price**
* **Product Info** (facts expander section)
* **Additional Details** (product facts grid)
* **Product Details** (detail bullets)
* **Product Link**
* **ASIN**
* **Image Links** (resized URLs)

Extracted data is saved to `product_data.csv`, and any failed URLs are recorded in `failed_links.txt`.

---

## 2. File Structure

```
/ (project root)
│
├─ scraper.py           # Main Python scraping script
├─ urls.txt             # Newline-separated list of ASINs
├─ product_data.csv     # Output CSV with scraped data
├─ failed_links.txt     # ASINs/URLs that failed during scraping
├─ requirements.txt     # Python dependencies (Selenium, BeautifulSoup4, etc.)
└─ README.md            # This documentation and usage guide
```

---

## 3. Dependencies & Setup

1. **Python 3.7+**
2. **Google Chrome** installed on the system
3. **Chromedriver** matching your Chrome version (ensure `chromedriver` is in PATH)

Install Python packages via pip:

```bash
pip install selenium beautifulsoup4 requests
```

Optionally, pin versions in `requirements.txt`:

```
selenium>=4.0.0
beautifulsoup4>=4.9.0
requests>=2.25.0
```

---

## 4. Script Breakdown (`scraper.py`)

### 4.1 Imports & Configuration

```python
import csv, re, time, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

* **csv**: Read/write CSV files
* **re**: Regular expressions to modify image URLs
* **time**: Sleep intervals
* **requests & BeautifulSoup**: (Imported but unused; can be removed or expanded)
* **selenium.webdriver**: Browser automation

Chrome is launched in incognito mode:

```python
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
driver = webdriver.Chrome(options=chrome_options)
```

### 4.2 URL List Handling

Reads ASINs from `urls.txt`, constructs product page URLs:

```python
with open('urls.txt') as f:
    asins = f.read().splitlines()
for asin in asins:
    url = f"https://www.amazon.in/dp/{asin}"
```

### 4.3 `replace_substr_in_url` Function

Uses regex to replace Amazon image size tokens in URLs for consistent resolution:

```python
def replace_substr_in_url(url):
    pattern = r'_SX\d+_SY\d+_CR,\d+,\d+,\d+,\d+_'
    return re.sub(pattern, '_SX689_', url)
```

### 4.4 Main Scraping Loop

For each URL:

1. **Navigate** to the page (`driver.get(url)`).
2. **Wait** 2 seconds for dynamic content.
3. **Extract Elements** using Selenium locators:

   * Title (`By.ID, 'title'`)
   * Info (`By.ID, 'productFactsDesktopExpander'`)
   * Additional details (`By.CLASS_NAME, 'a-fixed-left-grid.product-facts-detail'`)
   * Product details (`By.ID, 'detailBullets_feature_div'`)
   * Price (`By.ID, 'corePrice_feature_div'`)
   * Image elements via XPath and `WebDriverWait`
4. **Clean & Modify** image URLs with `replace_substr_in_url`.
5. **Write** collected data to CSV row.
6. **Error Handling**: On exceptions, log URL to `failed_links.txt` and continue.

Example CSV header:

```
Title,Product_price,Info,Additional Details,Product Details,Product_link,Asin,Image Link
```

---

## 5. Usage Instructions

1. **Populate** `urls.txt` with one ASIN per line.
2. **Ensure** `chromedriver` is installed and matches Chrome version.
3. **Install** Python dependencies.
4. **Run** the script:

   ```bash
   python scraper.py
   ```
5. **Review** `product_data.csv` and `failed_links.txt` after completion.

---

## 6. Error Handling

* **Element Not Found**: Catches exceptions when locators fail and records the URL.
* **Timeouts**: `WebDriverWait` ensures image elements are present; logs if they time out.
* **Network Issues**: Current script does not retry; consider wrapping navigation in a retry loop.

---

## 7. Customization & Extensions

* **Headless Mode**: Add `chrome_options.add_argument('--headless')` for non-GUI runs.
* **Proxy Support**: Configure Selenium capabilities for proxy rotation.
* **Requests + BeautifulSoup**: Switch to pure HTTP scraping for faster runs (if Amazon page structure allows).
* **Parallelization**: Use `concurrent.futures` to scrape multiple ASINs concurrently.
* **Data Storage**: Integrate with databases (SQLite, PostgreSQL) instead of CSV.

---

## 8. SEO Keywords


amazon scraper python
selenium amazon scraper
amazon product data extraction
amazon.in scraper
python csv scraper
web automation selenium
replace substr regex python
timeout wait selenium
dynamic web scraping amazon


---

*© 2025 Smaron Biswas. Licensed under MIT.*
