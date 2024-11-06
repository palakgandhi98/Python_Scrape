import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch the HTML content of a page
def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    return response.text

# Function to parse the HTML content and extract product data
def parse_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract product data
    product_data = [
        {
            "Product_Name": container.find("span", class_="a-size-base-plus a-color-base a-text-normal").get_text(strip=True) if container.find("span", class_="a-size-base-plus a-color-base a-text-normal") else " ",
            "Product_Price": container.find("span", class_="a-price-whole").get_text(strip=True) if container.find("span", class_="a-price-whole") else " ",
            "Product_Ratings": container.find("span", class_="a-icon-alt").get_text(strip=True) if container.find("span", class_="a-icon-alt") else " "
        }
        for container in soup.find_all("div", class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis puis-v3qvfbr6wwzu97251ibrrzrqee1 s-latency-cf-section puis-card-border")
    ]
    return product_data

# Function to scrape multiple pages
def scrape_multiple_pages(base_url, num_pages):
    all_product_data = []

    for page_num in range(1, num_pages + 1):
        print(f"Scraping page {page_num}...")
        url = f"{base_url}&page={page_num}"
        html_content = fetch_page(url)
        page_data = parse_page(html_content)
        all_product_data.extend(page_data)
    
    return all_product_data

# Base URL for the first page
base_url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

# Scrape 10 pages
product_data = scrape_multiple_pages(base_url, 10)

# Write data to CSV
with open("products_more.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Product_Name", "Product_Price", "Product_Ratings"])
    writer.writeheader()
    writer.writerows(product_data)

print("Data has been written to products.csv")
