import json
import sqlite3
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import JSONResponse

DB_NAME = "articles.db"
app = FastAPI()


# ex: frequencies/2025-10-17
@app.get("/frequencies/{date}")
def frequencies(date: str):
    db_conn = sqlite3.connect(DB_NAME)
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT nouns_frequencies FROM nouns_frequencies WHERE date LIKE ?",
        (f"{date}%",),
    )
    frequencies = cursor.fetchall()
    if frequencies:
        return json.loads(frequencies[0][0])
    return "Not available"
