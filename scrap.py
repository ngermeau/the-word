from feedparser import parse
from datetime import datetime
from hashlib import md5
from collections import Counter
from anthropic import Anthropic
import sqlite3


rss_urls = {
    "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "washingtonpost": "https://feeds.washingtonpost.com/rss/homepage/",
    "timesofindia": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
}


def init_database():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
        id TEXT PRIMARY KEY,
        title TEXT,
        source TEXT,
        date DATETIME
        )
    """)
    conn.commit()


def scrap_and_insert():
    articles = []
    for key, value in rss_urls.items():
        feed = parse(value)
        for entry in feed.entries[:10]:
            articles.append(
                {
                    "id": md5(f"{entry.title}{key}".encode()).hexdigest(),
                    "title": entry.title,
                    "source": key,
                    "date": datetime.now().isoformat(),
                }
            )
    cursor = conn.cursor()
    print(articles)
    cursor.executemany(
        "INSERT OR IGNORE INTO articles (id, title, source, date) VALUES (:id, :title, :source, :date)",
        articles,
    )
    conn.commit()


conn = sqlite3.connect("myapp.db")
init_database()
scrap_and_insert()
cursor = conn.cursor()
cursor.execute("SELECT * FROM articles")
print(cursor.fetchall())

# concat = " ".join(article["title"] for article in articles)
# print(concat)

# client = Anthropic(
#     api_key="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"
# )
# message = client.messages.create(
#     model="claude-sonnet-4-5-20250929",
#     max_tokens=1024,
#     messages=[
#         {
#             "role": "user",
#             "content": f"keep the text as is but only keep proper nouns and common nouns, remove auxiliary, verbs, prepositions, articles and separate with a comma: {concat}",
#         }
#     ],
# )


# cursor.execute("SELECT * FROM articles")
# print(cursor.fetchall())
# # answer = message.content[0].text
# # print(answer)
# # word_freq = Counter(answer.split(","))
# # print(answer)
# # print(word_freq)  # Word frequencies
# # print(len(word_freq))  # Number of unique words
