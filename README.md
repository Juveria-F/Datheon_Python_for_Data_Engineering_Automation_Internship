# Autonomous Web Scraper & Data Extractor

## Project Description
This project is a Python-based web scraper that extracts structured data from multiple pages of a website using Requests and BeautifulSoup4.

## Technologies Used
- Python 3
- Requests
- BeautifulSoup4
- CSV
- JSON

## Features
- Extracts book titles and prices.
- Collects availability and ratings.
- Supports automatic pagination.
- Handles errors and retries.
- Exports data into CSV and JSON files.
- Extracts at least 100 records.

## Website Used
https://books.toscrape.com/

## Output Files
1. products.csv
2. products.json

## How to Run

Install the required libraries:

```bash
pip install requests beautifulsoup4
```

Execute the program:

```bash
python scraper.py
```

## Result
Successfully extracted 100 book records and saved them in CSV and JSON formats.