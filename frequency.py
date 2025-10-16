from datetime import datetime
from collections import Counter
import nltk
import sqlite3
from nltk import pos_tag, word_tokenize

nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")


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
        if (tag.startswith("NN") and word.isalnum() and word != "s")
    ]

    return verbs_and_nouns


def get_today_words_frequency(db_conn):
    today = datetime.now().strftime("%Y-%m-%d")
    articles_today = get_articles_by_date(db_conn, today)
    concatenated_titles = " ".join(article[1] for article in articles_today).lower()
    print(concatenated_titles)
    filtered_words = extract_verbs_and_nouns(concatenated_titles)
    return Counter(filtered_words)


DB_NAME = "articles.db"
db_conn = sqlite3.connect(DB_NAME)
words = get_today_words_frequency(db_conn)
print(words)
