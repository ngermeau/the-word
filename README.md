# The Word

A daily news word cloud. Every day, The Word pulls headlines from major international outlets (The Guardian, BBC, Financial Times, Al Jazeera, Times of India, Japan Times, …), translates non-English titles, extracts the most significant nouns, and renders them as a typographic word cloud — larger words appeared more frequently in the news that day.

**Stack:** SvelteKit, TypeScript, Supabase (Postgres), `compromise` for NLP, `@huggingface/transformers` (NLLB-200) for translation, `rss-parser` for feeds, GSAP for the entrance animation.

![The Word – 2026-03-01](screenshot.png)
