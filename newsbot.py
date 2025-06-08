'''from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# ==== SETUP CHROMEDRIVER ====
# Update this path to your actual chromedriver.exe location
chrome_driver_path = r"D:\Projects\HintIntel\chromedriver\chromedriver.exe"

# Chrome Options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")  # Uncomment to run headless

# Chrome Service
service = Service(executable_path=chrome_driver_path)

# Create WebDriver instance
driver = webdriver.Chrome(service=service, options=options)

# ==== FUNCTION TO SCRAPE NEWS ====
def fetch_top_news():
    print("\n🔍 Fetching top news headlines...\n")

    # Go to Google News
    driver.get("https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en")
    time.sleep(3)  # wait for page to load fully

    # Find headline elements by updated CSS selector
    headlines = driver.find_elements(By.CSS_SELECTOR, 'a.DY5T1d')

    if not headlines:
        print("⚠️ No headlines found. Check the page structure.")
        return

    # Print top 10 headlines
    for i, headline in enumerate(headlines[:10], start=1):
        print(f"{i}. {headline.text}")

# ==== MAIN PROGRAM ====
if __name__ == "__main__":
    try:
        fetch_top_news()
    finally:
        print("\n✅ Done. Closing the browser.")
        driver.quit()
        '''
'''                                                     THE LOADSTAR                                                               '''

'''
import feedparser
from bs4 import BeautifulSoup

def clean_html_summary(html_summary, max_words=150):
    # Parse HTML and extract plain text
    soup = BeautifulSoup(html_summary, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    # Remove footer starting from "The post"
    footer_index = text.find("The post")
    if footer_index != -1:
        text = text[:footer_index].strip()
    
    # Optionally trim to max_words
    words = text.split()
    if len(words) > max_words:
        text = ' '.join(words[:max_words]) + '...'
    
    return text

def fetch_logistics_news():
    rss_url = "https://theloadstar.com/feed/"
    feed = feedparser.parse(rss_url)
    
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        raw_summary = entry.summary if 'summary' in entry else "No summary available"
        
        clean_summary = clean_html_summary(raw_summary)
        
        print(f"Title: {title}\n")
        print(f"Summary: {clean_summary}\n")
        print(f"Link: {link}\n")
        print("-" * 80)

if __name__ == "__main__":
    fetch_logistics_news()
    '''
'''                                       SUPPLY CHAIN DIGITAL(DIDNT HAVE ANY ENRRY THO)                                  '''
'''
import feedparser
from bs4 import BeautifulSoup

def clean_html_summary(html_summary, max_words=150):
    soup = BeautifulSoup(html_summary, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    # Remove footer starting from "The post"
    footer_index = text.find("The post")
    if footer_index != -1:
        text = text[:footer_index].strip()
    words = text.split()
    if len(words) > max_words:
        text = ' '.join(words[:max_words]) + '...'
    return text

def fetch_supply_chain_digital_news():
    rss_url = "https://supplychaindigital.com/rss"
    feed = feedparser.parse(rss_url)

    print("=== Supply Chain Digital ===\n")
    print(f"Total entries found: {len(feed.entries)}\n")

    if len(feed.entries) == 0:
        print("⚠️ No articles found or failed to parse.\n")
        return

    for entry in feed.entries[:2]:  # top 2 news
        title = entry.title
        link = entry.link
        raw_summary = entry.summary if 'summary' in entry else "No summary available"
        clean_summary = clean_html_summary(raw_summary)

        print(f"Title: {title}\n")
        print(f"Summary: {clean_summary}\n")
        print(f"Link: {link}\n")
        print("-" * 100)

if __name__ == "__main__":
    fetch_supply_chain_digital_news()

'''

'''                                                     LOGISTICS VIEWPOINTS                    '''

'''
import feedparser
from bs4 import BeautifulSoup

def clean_html_summary(html_summary, max_words=150):
    soup = BeautifulSoup(html_summary, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    footer_index = text.find("The post")
    if footer_index != -1:
        text = text[:footer_index].strip()
    words = text.split()
    if len(words) > max_words:
        text = ' '.join(words[:max_words]) + '...'
    return text

def fetch_logistics_viewpoints_news():
    rss_url = "https://logisticsviewpoints.com/feed/"
    feed = feedparser.parse(rss_url)

    print("=== Logistics Viewpoints ===\n")
    print(f"Total entries found: {len(feed.entries)}\n")

    if len(feed.entries) == 0:
        print("⚠️ No articles found or failed to parse.\n")
        return

    for entry in feed.entries[:2]:  # top 2 news
        title = entry.title
        link = entry.link
        raw_summary = entry.summary if 'summary' in entry else "No summary available"
        clean_summary = clean_html_summary(raw_summary)

        print(f"Title: {title}\n")
        print(f"Summary: {clean_summary}\n")
        print(f"Link: {link}\n")
        print("-" * 100)

if __name__ == "__main__":
    fetch_logistics_viewpoints_news()

    '''

import feedparser
from bs4 import BeautifulSoup

def clean_html_summary(html_summary, max_words=150):
    soup = BeautifulSoup(html_summary, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    # Remove footer or trailing text starting from "The post"
    footer_index = text.find("The post")
    if footer_index != -1:
        text = text[:footer_index].strip()
    
    words = text.split()
    if len(words) > max_words:
        text = ' '.join(words[:max_words]) + '...'
    return text

def fetch_news_from_rss(rss_url, source_name, max_articles=3):
    print(f"=== {source_name} ===\n")
    feed = feedparser.parse(rss_url)
    entries = feed.entries
    
    if not entries:
        print("⚠️ No articles found or failed to parse.\n")
        return
    
    print(f"Total entries found: {len(entries)}\n")
    
    for entry in entries[:max_articles]:
        title = entry.title if 'title' in entry else "No title"
        link = entry.link if 'link' in entry else "No link"
        raw_summary = entry.summary if 'summary' in entry else "No summary available"
        summary = clean_html_summary(raw_summary)
        
        print(f"Title: {title}\n")
        print(f"Summary: {summary}\n")
        print(f"Link: {link}\n")
        print("-" * 100)

if __name__ == "__main__":
    rss_feeds = [
        ("Supply Chain Management Review", "https://www.scmr.com/feed"),
        ("Transport Topics", "https://www.ttnews.com/rss.xml/"),
        ("FreightWaves", "https://www.freightwaves.com/feed"),
        ("Logistics Management", "https://feeds.feedburner.com/logisticsmgmt/latest"),
        ("Journal of Commerce", "https://joc.com/rssfeed"),
        ("The Loadstar", "https://theloadstar.com/feed/"),
    ]

    for source_name, rss_url in rss_feeds:
        fetch_news_from_rss(rss_url, source_name)

