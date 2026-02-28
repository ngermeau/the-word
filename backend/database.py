import logging
import sqlite3

DB_NAME = "theword.db"

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def db_connection():
    return sqlite3.connect(DB_NAME)


def init_daily_articles_table():
    logger.info("### Creating daily_articles table if none existent")
    db_conn = db_connection()
    cursor = db_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_articles (
        id TEXT PRIMARY KEY,
        title TEXT,
        source TEXT,
        date DATETIME
        )
    """)
    db_conn.commit()
    db_conn.close()


def init_daily_articles_analysis_table():
    logger.info("### Creating daily_articles_analysis table if none existent")
    db_conn = db_connection()
    cursor = db_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_articles_analysis(
        date DATETIME PRIMARY KEY,
        proper_nouns TEXT,
        proper_nouns_count TEXT,
        common_nouns TEXT,
        common_nouns_count TEXT
        )
    """)
    db_conn.commit()
    db_conn.close()


if __name__ == "__main__":
    logger.info("### DATABASE INIT")
    init_daily_articles_table()
    init_daily_articles_analysis_table()
    logger.info("")
