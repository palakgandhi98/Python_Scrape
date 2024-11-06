import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Download the HTML content from the URL and save it to a file
url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5"
}

response = requests.get(url, headers=headers)
with open("Amazon.html", "w", encoding="utf-8") as file:
    file.write(response.text)

# Step 2: Parse the saved HTML file with BeautifulSoup
with open("Amazon.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Step 3: Extract product data
product_data = [
    {
        "Product_Name": container.find("span", class_="a-size-base-plus a-color-base a-text-normal").get_text(strip=True) if container.find("span", class_="a-size-base-plus a-color-base a-text-normal") else " ",
        "Product_Price": container.find("span", class_="a-price-whole").get_text(strip=True) if container.find("span", class_="a-price-whole") else " ",
        "Product_Ratings": container.find("span", class_="a-icon-alt").get_text(strip=True) if container.find("span", class_="a-icon-alt") else " "
    }
    for container in soup.find_all("div", class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis puis-v3qvfbr6wwzu97251ibrrzrqee1 s-latency-cf-section puis-card-border")
]

# Step 4: Write data to CSV
with open("products.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Product_Name", "Product_Price", "Product_Ratings"])
    writer.writeheader()
    writer.writerows(product_data)

print("Data has been written to products.csv")
