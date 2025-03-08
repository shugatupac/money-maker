import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
from scraper.scraper import scrape_trending_products
from analysis.analyzer import analyze_opportunities
import logging

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)  # Create logs/ directory if it doesn’t exist
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "opportunities.db")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/opportunities')
def get_opportunities():
    logger.info("API request received for /api/opportunities")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT name, price, timestamp FROM opportunities ORDER BY price ASC")
        rows = c.fetchall()
        logger.info(f"Returning {len(rows)} opportunities")
        return jsonify([{"name": row[0], "price": f"${row[1]:.2f}", "timestamp": row[2]} for row in rows])
    except sqlite3.Error as e:
        logger.error(f"Database query failed: {e}")
        return jsonify([]), 500
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        logger.info("Database not found. Initializing...")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE opportunities (name TEXT, price REAL, timestamp TEXT)''')
        conn.commit()
        conn.close()
    app.run(host="0.0.0.0", port=5000)