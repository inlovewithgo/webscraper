from loguru import logger

def setup_logging():
    logger.add("scraper.log", rotation="1 MB")
