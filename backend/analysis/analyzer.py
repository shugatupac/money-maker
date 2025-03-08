import pandas as pd
import logging
import os

# Ensure the logs directory exists
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)  # Create logs/ directory if it doesn't exist

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

def analyze_opportunities(data):
    if not data:
        logger.warning("No data to analyze")
        return []
    
    logger.info("Starting data analysis")
    df = pd.DataFrame(data)
    df["price"] = df["price"].str.replace("$", "").astype(float)
    opportunities = df[df["price"] < 50].sort_values(by="price")
    logger.info(f"Found {len(opportunities)} opportunities under $50")
    
    return opportunities.to_dict(orient="records")
