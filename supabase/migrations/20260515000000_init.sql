CREATE TABLE IF NOT EXISTS daily_articles (
    id TEXT PRIMARY KEY,
    title TEXT,
    source TEXT,
    date DATE
);

CREATE TABLE IF NOT EXISTS daily_articles_analysis (
    date DATE PRIMARY KEY,
    proper_nouns JSONB,
    proper_nouns_count JSONB,
    common_nouns JSONB,
    common_nouns_count JSONB
);
