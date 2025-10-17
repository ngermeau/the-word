from feedparser import parse
from datetime import datetime
import sqlite3
from hashlib import md5

rss_urls = {
    # United States
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "washingtonpost": "https://feeds.washingtonpost.com/rss/homepage/",
    "wsj": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "usatoday": "http://rssfeeds.usatoday.com/usatoday-NewsTopStories",
    "latimes": "https://www.latimes.com/rss2.0.xml",
    "nypost": "https://nypost.com/feed/",
    # United Kingdom
    "theguardian": "https://www.theguardian.com/world/rss",
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "telegraph": "https://www.telegraph.co.uk/rss.xml",
    "independent": "https://www.independent.co.uk/rss",
    "dailymail": "https://www.dailymail.co.uk/home/index.rss",
    # Asia
    "timesofindia": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "japantimes": "https://www.japantimes.co.jp/feed/",
    "scmp": "https://www.scmp.com/rss/91/feed",  # South China Morning Post
    # Middle East
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    # Canada
    "globeandmail": "https://www.theglobeandmail.com/arc/outboundfeeds/rss/",
    "nationalpost": "https://nationalpost.com/feed/",
    # Australia
    "theaustralian": "https://www.theaustralian.com.au/feed/",
    "smh": "https://www.smh.com.au/rss/feed.xml",  # Sydney Morning Herald
    # # News Agencies
    "reuters": "https://www.reuters.com/rssFeed/topNews",
    "ap": "https://apnews.com/apf-topnews",
    "afp": "https://www.afp.com/en/feed",
}

DB_NAME = "articles.db"
db_conn = sqlite3.connect(DB_NAME)
today = datetime.now().date().isoformat()

# Init database if not in existence
cursor = db_conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    title TEXT,
    source TEXT,
    date DATETIME
    )
""")
db_conn.commit()

# Fetch the articles and store into database
articles = []
for key, value in rss_urls.items():
    feed = parse(value)
    for entry in feed.entries:
        articles.append(
            {
                "id": md5(f"{entry.title}{key}{today}".encode()).hexdigest(),
                "title": entry.title,
                "source": key,
                "date": today,
            }
        )

cursor.executemany(
    "INSERT OR IGNORE INTO articles (id, title, source, date) VALUES (:id, :title, :source, :date)",
    articles,
)
db_conn.commit()
db_conn.close()
