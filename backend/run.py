# backend/run.py
import schedule
import time
from scraper.scraper import scrape_trending_products
from analysis.analyzer import analyze_opportunities
from api.app import init_db, save_to_db
import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def job():
    logger.info("Starting scheduled scraping job")
    try:
        data = scrape_trending_products()
        opportunities = analyze_opportunities(data)
        save_to_db(opportunities)
        logger.info(f"Scheduled job completed successfully with {len(opportunities)} opportunities")
    except Exception as e:
        logger.error(f"Job failed: {str(e)}")

init_db()
schedule.every(6).hours.do(job)
logger.info("Running initial scrape")
job()
logger.info("Starting scheduler")
try:
    while True:
        schedule.run_pending()
        logger.debug("Scheduler tick")
        time.sleep(60)
except KeyboardInterrupt:
    logger.info("Shutting down scheduler")