import requests
from bs4 import BeautifulSoup
import time
import logging
import os

# Ensure the logs directory exists
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)  # Create logs/ directory if it doesn’t exist

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def scrape_trending_products():
    url = "https://www.shein.co.uk/?msockid=28231cf6aff86ec80c7208d8aec06fe3"  # Test site
    headers = {"User-Agent": "Mozilla/5.0"}
    logger.info(f"Starting scrape of {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info("Successfully fetched page")
    except requests.RequestException as e:
        logger.error(f"Scraping failed: {e}")
        return []
    
    soup = BeautifulSoup(response.content, "html.parser")
    products = soup.select(".thumbnail")
    data = []
    for product in products:
        try:
            name = product.select_one(".title").text.strip()
            price = product.select_one(".price").text.strip()
            data.append({"name": name, "price": price, "timestamp": time.ctime()})
        except AttributeError as e:
            logger.warning(f"Failed to parse product: {e}")
    
    logger.info(f"Scraped {len(data)} products")
    return []
