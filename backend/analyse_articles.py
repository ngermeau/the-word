import json
import logging
from collections import Counter
from datetime import datetime

import spacy
from database import db_connection

# Use today as current iteration
today = datetime.now().date().isoformat()
counter_size = 100

#  Setup model for text analysis
nlp = spacy.load("en_core_web_sm")

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"### ANALYSING ARTICLES FOR {today}")
logger.info("")

# Get articles for today
logger.info("### GETTING TODAY ARTICLES")
db_conn = db_connection()
cursor = db_conn.cursor()
cursor.execute("SELECT title FROM daily_articles WHERE date LIKE ?", (f"{today}%",))
today_articles = cursor.fetchall()
logger.info(f"### {len(today_articles)} articles found in total")
db_conn.close()

logger.info("### ANALYSING")
# Concatenate into one string
logger.info("### Concatenating all articles")
concatenated_titles = " ".join(article[0] for article in today_articles)

logger.info("### Analysing nouns and verbs and counting")
nlp_document = nlp(concatenated_titles)
common_nouns = [token.text for token in nlp_document if token.pos_ == "NOUN"]
common_nouns_count = Counter(common_nouns).most_common(counter_size)
proper_nouns = [token.text for token in nlp_document if token.pos_ == "PROPN"]
proper_nouns_count = Counter(proper_nouns).most_common(counter_size)

logger.info(f"### SAVING INTO DATABASE FOR {today} ")
db_conn = db_connection()
cursor = db_conn.cursor()
cursor.execute(
    "INSERT OR REPLACE INTO daily_articles_analysis(date, proper_nouns, proper_nouns_count, common_nouns, common_nouns_count) VALUES (?, ?, ?, ?, ?)",
    (
        today,
        json.dumps(proper_nouns),
        json.dumps(proper_nouns_count),
        json.dumps(common_nouns),
        json.dumps(common_nouns_count),
    ),
)
db_conn.commit()
db_conn.close()
