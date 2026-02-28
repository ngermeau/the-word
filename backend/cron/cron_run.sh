#!/bin/bash

# Check if argument was provided
if [ -z "$1" ]; then
    echo "Usage: ./run.sh <argument>"
    exit 1
fi

# Navigate to the script's directory
cd "$(dirname "$0")"

# Activate virtual environment and run the script
source venv/bin/activate

if [ "$1" = "fetch" ]; then
    python3 fetch_articles.py
else
    python3 analyse_articles.py

deactivate
