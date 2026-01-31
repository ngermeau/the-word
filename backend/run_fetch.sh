#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Activate virtual environment and run the script
source venv/bin/activate
python3 fetch_articles.py
deactivate
