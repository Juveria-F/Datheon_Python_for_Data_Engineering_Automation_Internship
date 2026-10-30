
import requests
from bs4 import BeautifulSoup
import csv
import json
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Website URL
url = "https://books.toscrape.com/catalogue/page-1.html"

# Create session
session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

# Retry handling
retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

session.mount("https://", HTTPAdapter(max_retries=retry))

# Store extracted data
data = []

print("Starting Web Scraper...")

# Pagination loop
while url and len(data) < 100:

    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:

            title = book.h3.a["title"]

            price = book.find(
                "p", class_="price_color"
            ).text.strip()

            availability = book.find(
                "p", class_="instock availability"
            ).text.strip()

            rating = book.find(
                "p", class_="star-rating"
            )["class"][1]

            data.append({
                "Title": title,
                "Price": price,
                "Availability": availability,
                "Rating": rating
            })

            if len(data) >= 100:
                break

        print("Records collected:", len(data))

        # Find next page
        next_page = soup.find(
            "li", class_="next"
        )

        if next_page and len(data) < 100:
            next_link = next_page.a["href"]
            url = urljoin(url, next_link)
        else:
            url = None

    except requests.RequestException as e:
        print("Error:", e)
        break

# Save CSV file
if data:
    with open("products.csv", "w",
              newline="", encoding="utf-8-sig") as file:

        writer = csv.DictWriter(
            file, fieldnames=data[0].keys()
        )

        writer.writeheader()
        writer.writerows(data)

    # Save JSON file
    with open("products.json", "w",
              encoding="utf-8") as file:

        json.dump(data, file, indent=4)

    print("\nScraping Completed!")
    print("Total Records:", len(data))
    print("CSV file created successfully!")
    print("JSON file created successfully!")

else:
    print("No records extracted.")
