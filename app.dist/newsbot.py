import feedparser
import requests
from bs4 import BeautifulSoup
import re
import json

def extract_image(entry):
    """Extracts image from an RSS entry."""
    if 'media_content' in entry:
        return entry.media_content[0]['url']
    elif 'enclosure' in entry:
        return entry.enclosure.url
    elif 'summary' in entry:
        soup = BeautifulSoup(entry.summary, "html.parser")
        img = soup.find("img")
        if img:
            return img["src"]
    return None  # No image found

def fetch_rss_bbc():
    feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
    feed = feedparser.parse(feed_url)
    
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "image": extract_image(entry)
        })
    return articles

def fetch_nytimes_rss():
    feed_url = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in feed.entries:
        articles.append({
            "region": "World",
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "image": extract_image(entry)
        })
    return articles

def fetch_nytimes_africa():
    feed_url = "https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml"
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "region": "Africa",
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "image": extract_image(entry)
        })
    return articles

def fetch_nytimes_americas():
    feed_url = "https://rss.nytimes.com/services/xml/rss/nyt/Americas.xml"
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "region": "America",
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "image": extract_image(entry)
        })
    return articles

def fetch_nytimes_asiapac():
    feed_url = "https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml"
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "region": "AsiaPacific",
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "image": extract_image(entry)
        })
    return articles

def fetch_nytimes_europe():
    feed_url = "https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml"
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "region": "Europe",
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "image": extract_image(entry)
        })
    return articles

def fetch_nytimes_middleast():
    feed_url = "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml"
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "region": "MiddleEast",
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "image": extract_image(entry)
        })
    return articles

def fetch_all_nytimes_news():
    regions = {
        "World": fetch_nytimes_rss(),
        "Africa": fetch_nytimes_africa(),
        "Americas": fetch_nytimes_americas(),
        "AsiaPacific": fetch_nytimes_asiapac(),
        "Europe": fetch_nytimes_europe(),
        "MiddleEast": fetch_nytimes_middleast(),
    }

    all_articles = []
    for region, articles in regions.items():
        for article in articles:
            all_articles.append({
                "region": region,
                "title": article["title"],
                "link": article["link"],
                "description": article["description"],
                "image": article["image"]
            })

    return all_articles

def get_rusuk_cnn():
    r = requests.get("https://edition.cnn.com/world/europe/ukraine")
    soup = BeautifulSoup(r.content, "html.parser")
    d = soup.find("div", class_="container__field-links container_list-headlines__field-links")
    if d:
        data = d.text.splitlines()
        return [item for item in data if item]
    return []

