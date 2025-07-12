import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///olx_cars.db')
    
    # Scraping settings
    BASE_URL = "https://www.olx.pt/carros-motos-e-barcos/carros"
    DELAY_BETWEEN_REQUESTS = 2  # seconds
    MAX_PAGES = 10  # maximum pages to scrape per search
    
    # Headers to avoid being blocked
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Selenium settings
    SELENIUM_TIMEOUT = 10
    SELENIUM_IMPLICIT_WAIT = 5 