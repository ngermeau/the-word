# The Front Word - Frontend

Interactive word cloud visualization of the most frequent words in international news headlines.

## Overview

This SvelteKit application displays word frequencies from global newspaper headlines as a dynamic word cloud. Words are placed on a 50x50 CSS grid using a custom layout algorithm that:

- Measures each word's dimensions based on its frequency
- Finds available positions trying horizontal then vertical orientations
- Scales font size proportionally to word frequency
- Highlights high-frequency words (>10 occurrences) with inverted colors

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Or open in browser automatically
npm run dev -- --open
```

The app runs at `http://localhost:5173` by default.

## Project Structure

```
frontend/
├── src/
│   ├── lib/
│   │   └── utils.ts      # Grid layout algorithm
│   └── routes/
│       ├── +page.svelte  # Main word cloud component
│       └── +page.server.ts # Server-side data loading
├── static/
└── package.json
```

## How It Works

1. Server loads word frequencies from the backend API
2. Words are shuffled randomly for varied layouts
3. Each word is measured using a hidden DOM element
4. The algorithm finds the first available grid position
5. Words are rendered with font size based on frequency
