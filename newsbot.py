
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

