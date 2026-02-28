import json

from database import db_connection
from fastapi import FastAPI, HTTPException

app = FastAPI()


# ex: theword/2025-10-17
@app.get("/theword/{date}")
def the_word(date: str):
    db_conn = db_connection()
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT proper_nouns_count FROM daily_articles_analysis WHERE date LIKE ?",
        (f"{date}%",),
    )
    db_result = cursor.fetchall()

    if not db_result:
        raise HTTPException(status_code=404, detail="No data for this date")

    result = json.loads(db_result[0][0])
    sorted_result = sorted(result, key=lambda x: x[1], reverse=True)
    if db_result:
        return {"data": sorted_result}
