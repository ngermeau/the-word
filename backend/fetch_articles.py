import logging
from datetime import datetime
from functools import partial
from hashlib import md5

import yaml
from database import db_connection
from feedparser import parse
from transformers import pipeline

# Use today as current iteration
today = datetime.now().date().isoformat()

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup model for translation
translator = pipeline(
    "translation", model="facebook/nllb-200-distilled-600M", device=-1
)
fr_to_en = partial(translator, src_lang="fra_Latn", tgt_lang="eng_Latn")
es_to_en = partial(translator, src_lang="spa_Latn", tgt_lang="eng_Latn")
de_to_en = partial(translator, src_lang="deu_Latn", tgt_lang="eng_Latn")
nl_to_en = partial(translator, src_lang="nld_Latn", tgt_lang="eng_Latn")
it_to_en = partial(translator, src_lang="ita_Latn", tgt_lang="eng_Latn")
pt_to_en = partial(translator, src_lang="por_Latn", tgt_lang="eng_Latn")
ar_to_en = partial(translator, src_lang="ara_Arab", tgt_lang="eng_Latn")


def translate_to_en(text, language):
    if language == "en":
        return text
    if language == "fr":
        return fr_to_en(text)[0]["translation_text"]
    elif language == "es":
        return es_to_en(text)[0]["translation_text"]
    elif language == "de":
        return de_to_en(text)[0]["translation_text"]
    elif language == "nl":
        return nl_to_en(text)[0]["translation_text"]
    elif language == "it":
        return it_to_en(text)[0]["translation_text"]
    elif language == "pt":
        return pt_to_en(text)[0]["translation_text"]
    elif language == "ar":
        return ar_to_en(text)[0]["translation_text"]
    else:
        return text


def insert_into_database(articles):
    db_conn = db_connection()
    cursor = db_conn.cursor()
    cursor.executemany(
        "INSERT OR IGNORE INTO daily_articles (id, title, source, date) VALUES (:id, :title, :source, :date)",
        articles,
    )
    logger.info(f"### Inserted {cursor.rowcount} new articles into database")
    db_conn.commit()
    db_conn.close()


logger.info(f"### FETCHING ARTICLES FOR {today}")
logger.info("")

# Fetch the articles and store into database
logger.info("### FETCHING ARTICLES")
with open("newspapers.yaml") as f:
    newspapers = yaml.safe_load(f)

total_articles = []
for newspaper in newspapers:
    articles = []
    source_name = newspaper["name"]
    rss_url = newspaper["rss_url"]
    language = newspaper["language"]
    logger.info(f"### Fetching {source_name}")
    feed = parse(rss_url)
    try:
        feed.channel.title  # Testing url is still working
    except AttributeError:
        logger.error(f"{source_name} rss url is failing")
        logger.info("")
        continue
    for entry in feed.entries:
        article_title = translate_to_en(entry.title, language)
        articles.append(
            {
                "id": md5(f"{article_title}{source_name}{today}".encode()).hexdigest(),
                "title": article_title,
                "source": source_name,
                "date": today,
            }
        )
    logger.info(f"### Found {len(articles)} articles for {source_name}")
    insert_into_database(articles)
    logger.info("")
