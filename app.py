'''import streamlit as st
import feedparser
from bs4 import BeautifulSoup

# Helper to clean summary
def clean_html_summary(html_summary, max_words=40):
    soup = BeautifulSoup(html_summary, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    footer_index = text.find("The post")
    if footer_index != -1:
        text = text[:footer_index].strip()
    words = text.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '...'
    return text

# Fetch and return news entries
def fetch_news(rss_url, max_articles=5):
    feed = feedparser.parse(rss_url)
    return feed.entries[:max_articles] if feed.entries else []

# Streamlit UI
st.set_page_config(layout="wide", page_title="Logistics News")
st.title("🗞️ Latest Logistics & Supply Chain News")

rss_feeds = [
    ("Supply Chain Management Review", "https://www.scmr.com/feed"),
    ("Transport Topics", "https://www.ttnews.com/rss.xml/"),
    ("FreightWaves", "https://www.freightwaves.com/feed"),
    ("Logistics Management", "https://feeds.feedburner.com/logisticsmgmt/latest"),
    ("Journal of Commerce", "https://joc.com/rssfeed"),
    ("The Loadstar", "https://theloadstar.com/feed/")
]

for source_name, rss_url in rss_feeds:
    with st.expander(f"📌 {source_name}", expanded=True):
        news_items = fetch_news(rss_url)
        if not news_items:
            st.warning("No articles found.")
        for entry in news_items:
            st.markdown(f"### [{entry.title}]({entry.link})")
            summary = clean_html_summary(entry.summary if 'summary' in entry else "")
            st.markdown(f"➤ {summary}")
            st.markdown("---")

            '''
''' -------------------------------- THE MAIN ONE ----------------------------------------------'''
'''
import streamlit as st
import feedparser
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

st.set_page_config(layout="wide")
st.title("📦 Logistics & Supply Chain News Dashboard")

# Clean up the HTML and trim the summary
def clean_summary(html_summary, max_words=40):
    soup = BeautifulSoup(html_summary, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    footer_index = text.find("The post")
    if footer_index != -1:
        text = text[:footer_index]
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return text

# Try to fetch thumbnail from the actual article page
def fetch_thumbnail(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.content, "html.parser")
        img = soup.find("meta", property="og:image")
        if img and img.get("content"):
            return img["content"]
        img = soup.find("img")
        if img and img.get("src"):
            return urljoin(url, img["src"])
    except:
        return None
    return None

# Fetch and display articles from RSS
def display_news(rss_url, source_name):
    feed = feedparser.parse(rss_url)
    st.subheader(source_name)
    cols = st.columns(3)

    for i, entry in enumerate(feed.entries[:3]):
        title = entry.title
        link = entry.link
        summary = clean_summary(entry.summary if 'summary' in entry else "")
        published = entry.get("published", "No date")
        thumbnail = fetch_thumbnail(link) or "https://via.placeholder.com/150"

        with cols[i % 3]:
            st.markdown(f"""
                <div style='background-color:#f9f9f9; padding:10px; border-radius:10px; box-shadow:2px 2px 5px rgba(0,0,0,0.1);'>
                    <img src="{thumbnail}" style='width:100%; border-radius:10px; height:150px; object-fit:cover;'>
                    <h4 style='margin-top:10px;'>{title}</h4>
                    <p style='font-size:13px; color:grey;'>{published}</p>
                    <p>{summary}</p>
                    <a href="{link}" target="_blank">Read more →</a>
                </div>
            """, unsafe_allow_html=True)

# Define sources
rss_feeds = [
    ("Supply Chain Management Review", "https://www.scmr.com/feed"),
    ("Transport Topics", "https://www.ttnews.com/rss.xml/"),
    ("FreightWaves", "https://www.freightwaves.com/feed"),
    ("Logistics Management", "https://feeds.feedburner.com/logisticsmgmt/latest"),
    ("Journal of Commerce", "https://joc.com/rssfeed"),
    ("The Loadstar", "https://theloadstar.com/feed/")
]

# Loop through each source
for name, url in rss_feeds:
    display_news(url, name)
    '''
''' ----------------------------------------------------------------------------------------------'''

import streamlit as st
import feedparser
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

st.set_page_config(layout="wide")
st.title("🗞️ News Dashboard")

# Clean up the HTML and trim the summary
def clean_summary(html_summary, max_words=40):
    soup = BeautifulSoup(html_summary, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    footer_index = text.find("The post")
    if footer_index != -1:
        text = text[:footer_index]
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return text

# Try to fetch thumbnail from the actual article page
def fetch_thumbnail(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.content, "html.parser")
        img = soup.find("meta", property="og:image")
        if img and img.get("content"):
            return img["content"]
        img = soup.find("img")
        if img and img.get("src"):
            return urljoin(url, img["src"])
    except:
        return None
    return None

# Fetch and display articles from RSS
def display_news(rss_url, source_name):
    feed = feedparser.parse(rss_url)
    st.subheader(f"📌 {source_name}")
    
    if not feed.entries:
        st.warning("No articles found for this source.")
        return
    
    cols = st.columns(3)

    for i, entry in enumerate(feed.entries[:3]):
        title = entry.title if hasattr(entry, 'title') else "No Title Available"
        link = entry.link if hasattr(entry, 'link') else "#"
        summary = clean_summary(entry.summary if hasattr(entry, 'summary') else "No summary available")
        published = entry.get("published", "No date")
        thumbnail = fetch_thumbnail(link) or "https://via.placeholder.com/300x200/cccccc/666666?text=News"

        with cols[i % 3]:
            # Use Streamlit components instead of pure HTML
            with st.container():
                st.image(thumbnail, use_column_width=True)
                st.markdown(f"**{title[:80]}{'...' if len(title) > 80 else ''}**")
                st.caption(published)
                st.write(summary)
                st.markdown(f"[Read more →]({link})")
                st.markdown("---")

# Define sources
rss_feeds = [
    ("Supply Chain Management Review", "https://www.scmr.com/feed"),
    ("Transport Topics", "https://www.ttnews.com/rss.xml/"),
    ("FreightWaves", "https://www.freightwaves.com/feed"),
    ("Logistics Management", "https://feeds.feedburner.com/logisticsmgmt/latest"),
    ("Journal of Commerce", "https://joc.com/rssfeed"),
    ("The Loadstar", "https://theloadstar.com/feed/")
]

# Loop through each source
for name, url in rss_feeds:
    display_news(url, name)
    st.markdown("---")  # Add separator between sources

