# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Front Word is a news aggregation and visualization project that fetches articles from international news sources, analyzes word frequencies in headlines using NLP, and displays them as an interactive word cloud.

**Architecture:**
- **Backend (Python)**: RSS feed fetching, NLP processing, SQLite storage, FastAPI server
- **Frontend (SvelteKit)**: Interactive word cloud visualization with custom grid layout algorithm

## Common Commands

### Backend (Python)

```bash
# Setup (first time)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Fetch articles from RSS feeds
./run_fetch.sh
# Or manually:
cd backend && source venv/bin/activate && python3 fetch_articles.py

# Calculate word frequencies
./run_frequency.sh
# Or manually:
cd backend && source venv/bin/activate && python3 calculate_frequency.py

# Run API server
cd backend && source venv/bin/activate && uvicorn api:app --reload
```

### Frontend (SvelteKit)

```bash
# Install dependencies
cd frontend
npm install

# Development server
npm run dev
# Or with browser auto-open:
npm run dev -- --open

# Type checking
npm run check

# Linting and formatting
npm run lint
npm run format

# Production build
npm run build
npm run preview
```

## Architecture Details

### Data Flow

1. **RSS Fetching** (`fetch_articles.py`):
   - Fetches from multiple international sources (Guardian, BBC, FT, Al Jazeera, Times of India, Japan Times)
   - Uses MD5 hash of `{title}{source}{date}` as unique ID
   - Stores in SQLite `articles` table with columns: `id`, `title`, `source`, `date`

2. **Frequency Analysis** (`calculate_frequency.py`):
   - Extracts nouns from article titles using NLTK POS tagging
   - Filters for proper nouns (NN* tags), alphanumeric only
   - Stores top 200 words in `frequencies` table as JSON array of `[word, count]` tuples
   - Note: NLTK downloads (`punkt_tab`, `averaged_perceptron_tagger_eng`) must be run once

3. **API** (`api.py`):
   - FastAPI endpoint: `GET /frequencies/{date}` (format: YYYY-MM-DD)
   - Returns JSON array of `[word, count]` tuples or "Not available"
   - **Known Issue**: Code references `nouns_frequencies` table but schema uses `frequencies` table

4. **Frontend Visualization**:
   - Custom grid-based word cloud algorithm (`utils.js`)
   - 50x50 CSS grid with dynamic cell sizing
   - Words placed sequentially trying horizontal/vertical orientations
   - Font size scales with frequency, high-frequency words (>8) get black background
   - Grid collision detection prevents word overlap

### Key Files

- `backend/fetch_articles.py`: RSS feed definitions and article fetching logic
- `backend/calculate_frequency.py`: NLP processing with NLTK
- `backend/api.py`: FastAPI server with frequency endpoint
- `frontend/src/lib/utils.js`: Grid layout algorithm with collision detection
- `frontend/src/routes/+page.svelte`: Main visualization component

### Database Schema

```sql
-- articles table
CREATE TABLE articles (
    id TEXT PRIMARY KEY,
    title TEXT,
    source TEXT,
    date DATETIME
);

-- frequencies table
CREATE TABLE frequencies (
    date DATETIME PRIMARY KEY,
    words TEXT  -- JSON array of [word, count] tuples
);
```

### Known Issues

- **API/DB mismatch**: `api.py` queries `nouns_frequencies` table but schema defines `frequencies` table
- **Missing comma**: `fetch_articles.py:10` has syntax error (missing comma after Financial Times URL)
- Frontend currently uses static data (`newdata.json`) instead of API endpoint
