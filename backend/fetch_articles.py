import json
import logging
import sqlite3
from datetime import datetime
from hashlib import md5

from feedparser import parse
from functools import partial
from transformers import pipeline

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup model for translation
translator = pipeline(
    "translation", model="facebook/nllb-200-distilled-600M", device=-1
)
fr_to_en = partial(translator, src_lang="fra_Latn", tgt_lang="eng_Latn")
es_to_en = partial(translator, src_lang="spa_Latn", tgt_lang="eng_Latn")

def translate_to_en(text, language):
    if language == "en":
        return text
    if language == "fr":
        return fr_to_en(text)[0]['translation_text']
    elif language == "es":
        return es_to_en(text)[0]['translation_text']
    elif language == "de":
        return de_to_en(text)[0]['translation_text']
    else:
        return text

# Open database connection
DB_NAME = "articles.db"
db_conn = sqlite3.connect(DB_NAME)

# Init database if not in existence
logger.info("### Creating table if none existent ###")
cursor = db_conn.cursor()
_ = cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    title TEXT,
    source TEXT,
    date DATETIME
    )
""")
db_conn.commit()
logger.info("")

# Fetch the articles and store into database
with open("newspapers.json") as f:
    newspapers = json.load(f)

today = datetime.now().date().isoformat()
total_articles = []
for newspaper in newspapers:
    articles = []
    source_name = newspaper["name"]
    rss_url = newspaper["rss_url"]
    language = newspaper["language"]
    logger.info(f"### Fetching {source_name} ###")
    feed = parse(rss_url)
    try:
        feed.channel.title # Testing url is still working
    except AttributeError:
        logger.error(f"{source_name} rss url is failing")
        logger.info("")
        continue
    for entry in feed.entries:
        article_title =  translate_to_en(entry.title, language)
        articles.append(
            {
                "id": md5(f"{article_title}{source_name}{today}".encode()).hexdigest(),
                "title": article_title,
                "source": source_name,
                "date": today,
            }
        )
    logger.info(f"### Found {len(articles)} articles for {source_name}")
    total_articles += articles
    logger.info(f"### Found {len(total_articles)} articles in total")
    logger.info("")


# Insert articles in database
# cursor = db_conn.cursor()
# cursor.executemany(
#     "INSERT OR IGNORE INTO articles (id, title, source, date) VALUES (:id, :title, :source, :date)",
#     articles,
# )
# print(cursor.rowcount)
# db_conn.commit()
# db_conn.close()
