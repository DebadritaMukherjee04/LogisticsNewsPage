import streamlit as st
import feedparser
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

st.set_page_config(layout="wide")
st.title("🗞️ News Dashboard")

# Cleaning up the HTML and trimming the summary
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

# Fetching thumbnail from the actual article page
def fetch_thumbnail(url):
    try:
        res = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        if res.status_code != 200:
            return None
            
        soup = BeautifulSoup(res.content, "html.parser")
        
        # Try to find Open Graph image first
        img = soup.find("meta", property="og:image")
        if img and img.get("content"):
            img_url = img["content"]
            # Validate the image URL
            if img_url.startswith(('http://', 'https://')):
                return img_url
        
        # Try to find first img tag as fallback
        img = soup.find("img")
        if img and img.get("src"):
            img_url = urljoin(url, img["src"])
            if img_url.startswith(('http://', 'https://')):
                return img_url
                
    except Exception as e:
        print(f"Error fetching thumbnail for {url}: {e}")
        return None
    return None

# Function to validate if image URL is accessible
def is_valid_image_url(url):
    try:
        if not url or not url.startswith(('http://', 'https://')):
            return False
        response = requests.head(url, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
        content_type = response.headers.get('content-type', '')
        return response.status_code == 200 and content_type.startswith('image/')
    except:
        return False

# Fetching and displaying articles from RSS
def display_news(rss_url, source_name):
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        st.error(f"Error parsing RSS feed for {source_name}: {e}")
        return
        
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
        
        # Get thumbnail with better error handling
        thumbnail = None
        if link != "#":
            thumbnail = fetch_thumbnail(link)
        
        # Use a reliable placeholder if no valid thumbnail found
        placeholder_url = "https://via.placeholder.com/300x200/e1e5e9/6c757d?text=News+Article"
        
        if thumbnail and is_valid_image_url(thumbnail):
            image_url = thumbnail
        else:
            image_url = placeholder_url

        with cols[i % 3]:
            with st.container():
                try:
                    st.image(image_url, use_container_width=True)
                except Exception as e:
                    # If image still fails, show a text placeholder
                    st.info("📰 Image not available")
                    print(f"Image display error: {e}")
                    
                st.markdown(f"**{title[:80]}{'...' if len(title) > 80 else ''}**")
                st.caption(published)
                st.write(summary)
                if link != "#":
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
    try:
        display_news(url, name)
        st.markdown("---")  # Add separator between sources
    except Exception as e:
        st.error(f"Error processing {name}: {e}")
        continue
