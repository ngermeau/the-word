from datetime import datetime
from collections import Counter
import sqlite3
import nltk
from nltk import pos_tag, word_tokenize

nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")


def init_database(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS word_frequencies(
        date DATETIME PRIMARY KEY,
        word_counts TEXT,
        )
    """)
    db_conn.commit()


def get_articles_by_date(db_conn, date_str):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE date LIKE ?", (f"{date_str}%",))
    return cursor.fetchall()


def extract_verbs_and_nouns(text):
    """Extract only verbs and nouns from text using NLTK POS tagging"""
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    verbs_and_nouns = [
        word
        for word, tag in tagged
        if (tag.startswith("NN") and word.isalnum() and word != "s" and word != "i")
    ]

    return verbs_and_nouns


def get_frequencies_of_words(db_conn, date):
    articles_today = get_articles_by_date(db_conn, date)
    concatenated_titles = " ".join(article[1] for article in articles_today).lower()
    filtered_words = extract_verbs_and_nouns(concatenated_titles)
    return Counter(filtered_words)

def store(frequencies_of_words,date):
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO word_frequencies(date, word_counts) VALUES (?, ?)", (today, json.dumps(frequencies_of_words))
    db_conn.commit()

DB_NAME = "articles.db"
db_conn = sqlite3.connect(DB_NAME)
today = datetime.now().strftime("%Y-%m-%d")
frequencies_of_words = get_frequencies_of_words(today,db_conn)
store(today,frequencies_of_words,db_conn)
