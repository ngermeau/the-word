# The Word

A news aggregation and visualization project that fetches headlines from international sources, analyzes word frequencies using NLP, and displays them as an interactive word cloud.

Every day, The Word pulls headlines from major international outlets (The Guardian, BBC, Financial Times, Al Jazeera, Times of India, Japan Times), extracts the most significant nouns using spaCy NLP, and renders them as a typographic word cloud — larger words appeared more frequently in the news that day.

**Stack:** Python, FastAPI, spaCy, feedparser, SQLite, SvelteKit

![The Word – 2026-03-01](screenshot.png)

---

## Installation

**Backend** (Python 3.10+):

```bash
cd backend && python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
uvicorn api:app --reload
```

Available at `GET /theword/{date}` — returns word frequencies for the given date (`YYYY-MM-DD`).

```json
{ "data": [["word", 42], ["word2", 31], ...] }
```

**Frontend** (Node 18+):

```bash
cd frontend && npm install && npm run dev
```

Available at `http://localhost:5173/{YYYY-MM-DD}`.

---

## Cron Usage

```bash
# Fetch articles
python3 fetch_articles.py

# Calculate word frequencies
python3 calculate_frequency.py

# Automate (crontab -e)
0 6,18 * * * /path/to/backend/cron_run.sh >> /path/to/backend/cron.log 2>&1
```
