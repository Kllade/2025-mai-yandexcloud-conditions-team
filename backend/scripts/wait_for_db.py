import time
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from api.core.config import settings

DATABASE_URL = settings.db.DATABASE_URL_psycopg2
MAX_RETRIES = 30  
RETRY_DELAY = 2   

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db():
    """Ожидание доступности базы данных"""
    logger.info("Checking database connection...")
    
    retries = 0
    while retries < MAX_RETRIES:
        try:
            engine = create_engine(DATABASE_URL)
            conn = engine.connect()
            conn.close()
            logger.info("Database is available!")
            return
        except OperationalError:
            retries += 1
            logger.info(f"Database unavailable, waiting {RETRY_DELAY} seconds... (attempt {retries}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    
    logger.error("Could not connect to database after multiple attempts")
    raise Exception("Database connection failed")

if __name__ == "__main__":
    wait_for_db()