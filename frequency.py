from datetime import datetime
from collections import Counter
import sqlite3
import json
from nltk import pos_tag, word_tokenize

# Download once, then comment out
# nltk.download("punkt_tab")
# nltk.download("averaged_perceptron_tagger_eng")

DB_NAME = "articles.db"
db_conn = sqlite3.connect(DB_NAME)
cursor = db_conn.cursor()
today = datetime.now().date().isoformat()

# Init database if none in existence
cursor.execute("""
    CREATE TABLE IF NOT EXISTS nouns_frequencies(
    date DATETIME PRIMARY KEY,
    nouns_frequencies TEXT
    )
""")
db_conn.commit()

# Get articles for today and concatenate in one long string
cursor.execute("SELECT title FROM articles WHERE date LIKE ?", (f"{today}%",))
today_articles = cursor.fetchall()
concatenated_titles = " ".join(article[0] for article in today_articles).lower()

# Keep only the nouns
tokens = word_tokenize(concatenated_titles)
tagged = pos_tag(tokens)
nouns = [
    word
    for word, tag in tagged
    if (tag.startswith("NN") and word.isalnum() and word != "s" and word != "i")
]

# Get the frequencies for the nouns
nouns_frequencies = Counter(nouns)
print(nouns_frequencies)

# Store into database for the current day
cursor.execute(
    "INSERT OR REPLACE INTO nouns_frequencies(date, nouns_frequencies) VALUES (?, ?)",
    (today, json.dumps(nouns_frequencies.most_common(100))),
)
db_conn.commit()

db_conn.close()
