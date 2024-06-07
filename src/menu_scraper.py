import requests 
from bs4 import BeautifulSoup 
from PIL import Image 
from io import BytesIO
import pytesseract 
import psycopg2
import time

# Configure Tesseract executable path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Database connection setup
conn = psycopg2.connect(
    dbname="menu_db",
    user="username",
    password="password",
    host="localhost"
)
cur = conn.cursor()

# Function to scrape menu images from restaurant websites
def scrape_menu_images(restaurant_urls):
    image_urls = []
    for url in restaurant_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Assuming images are in <img> tags with class 'menu-image'
        images = soup.find_all('img', class_='menu-image')
        for img in images:
            image_urls.append(img['src'])
    return image_urls

# Function to perform OCR on images and extract items and prices
def extract_items_prices(image_urls):
    items_prices = []
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        # Simple parsing assuming item and price on each line separated by a space
        for line in text.split('\n'):
            if line.strip():
                parts = line.rsplit(' ', 1)
                if len(parts) == 2:
                    item, price = parts
                    items_prices.append((item.strip(), price.strip()))
    return items_prices

# Function to store extracted items and prices in the database
def store_in_database(items_prices):
    for item, price in items_prices:
        cur.execute("INSERT INTO menu_items (item, price) VALUES (%s, %s)", (item, price))
    conn.commit()

# Main function
def main():
    restaurant_urls = [
        'http://example.com/restaurant1',
        'http://example.com/restaurant2',
        # Add more restaurant URLs here
    ]
    start_time = time.time()
    image_urls = scrape_menu_images(restaurant_urls)
    items_prices = extract_items_prices(image_urls)
    store_in_database(items_prices)
    end_time = time.time()

    print(f"Total time taken: {end_time - start_time} seconds")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()



