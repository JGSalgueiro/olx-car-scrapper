import time
import json
import re
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from config import Config
from models import CarListing, get_db
from datetime import datetime

class OLXScraper:
    def __init__(self):
        self.config = Config()
        self.ua = UserAgent()
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.implicitly_wait(self.config.SELENIUM_IMPLICIT_WAIT)
        
    def close_driver(self):
        """Close the webdriver"""
        if self.driver:
            self.driver.quit()
            
    def extract_price(self, price_text: str) -> tuple:
        """Extract price and currency from price text"""
        if not price_text:
            return None, None
            
        # Remove common price indicators
        price_text = price_text.replace('€', '').replace('EUR', '').strip()
        
        # Extract numbers
        numbers = re.findall(r'[\d,]+', price_text)
        if numbers:
            # Remove commas and convert to float
            price = float(numbers[0].replace(',', ''))
            return price, 'EUR'
        return None, None
        
    def extract_car_details(self, title: str) -> Dict:
        """Extract car details from title"""
        details = {
            'brand': None,
            'model': None,
            'year': None,
            'mileage': None,
            'fuel_type': None,
            'transmission': None
        }
        
        # Extract year
        year_match = re.search(r'\b(19|20)\d{2}\b', title)
        if year_match:
            details['year'] = int(year_match.group())
            
        # Extract mileage
        mileage_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*km', title, re.IGNORECASE)
        if mileage_match:
            mileage_str = mileage_match.group(1).replace(',', '')
            details['mileage'] = int(mileage_str)
            
        # Extract fuel type
        fuel_types = ['gasolina', 'diesel', 'híbrido', 'elétrico', 'gas', 'lpg']
        for fuel in fuel_types:
            if fuel.lower() in title.lower():
                details['fuel_type'] = fuel
                break
                
        # Extract transmission
        if 'automático' in title.lower() or 'automatic' in title.lower():
            details['transmission'] = 'Automatic'
        elif 'manual' in title.lower():
            details['transmission'] = 'Manual'
            
        return details
        
    def parse_listing_page(self, url: str) -> Optional[Dict]:
        """Parse individual listing page"""
        try:
            self.driver.get(url)
            time.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract basic info
            title_elem = soup.find('h1')
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # Extract price
            price_elem = soup.find('span', {'data-testid': 'ad-price'})
            price_text = price_elem.get_text(strip=True) if price_elem else ''
            price, currency = self.extract_price(price_text)
            
            # Extract location
            location_elem = soup.find('span', {'data-testid': 'location'})
            location = location_elem.get_text(strip=True) if location_elem else ''
            
            # Extract description
            desc_elem = soup.find('div', {'data-testid': 'ad-description'})
            description = desc_elem.get_text(strip=True) if desc_elem else ''
            
            # Extract seller info
            seller_elem = soup.find('span', {'data-testid': 'seller-name'})
            seller_name = seller_elem.get_text(strip=True) if seller_elem else ''
            
            # Extract images
            image_elements = soup.find_all('img', {'data-testid': 'ad-image'})
            image_urls = [img.get('src') for img in image_elements if img.get('src')]
            
            # Extract car details from title
            car_details = self.extract_car_details(title)
            
            # Extract OLX ID from URL
            olx_id_match = re.search(r'ID(\w+)', url)
            olx_id = olx_id_match.group(1) if olx_id_match else None
            
            return {
                'olx_id': olx_id,
                'title': title,
                'price': price,
                'currency': currency,
                'location': location,
                'description': description,
                'seller_name': seller_name,
                'url': url,
                'image_urls': json.dumps(image_urls),
                **car_details
            }
            
        except Exception as e:
            print(f"Error parsing listing page {url}: {e}")
            return None
            
    def get_listing_urls(self, search_url: str, max_pages: int = None) -> List[str]:
        """Get all listing URLs from search results"""
        if max_pages is None:
            max_pages = self.config.MAX_PAGES
            
        listing_urls = []
        page = 1
        
        while page <= max_pages:
            try:
                page_url = f"{search_url}?page={page}" if page > 1 else search_url
                self.driver.get(page_url)
                time.sleep(self.config.DELAY_BETWEEN_REQUESTS)
                
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find listing links
                listing_elements = soup.find_all('a', href=re.compile(r'/d/'))
                
                if not listing_elements:
                    print(f"No more listings found on page {page}")
                    break
                    
                page_urls = []
                for elem in listing_elements:
                    href = elem.get('href')
                    if href and '/d/' in href:
                        full_url = f"https://www.olx.pt{href}" if href.startswith('/') else href
                        page_urls.append(full_url)
                
                listing_urls.extend(page_urls)
                print(f"Found {len(page_urls)} listings on page {page}")
                
                page += 1
                
            except Exception as e:
                print(f"Error getting listings from page {page}: {e}")
                break
                
        return list(set(listing_urls))  # Remove duplicates
        
    def scrape_car_model(self, car_model: str) -> List[Dict]:
        """Scrape all listings for a specific car model"""
        search_url = f"{self.config.BASE_URL}/q-{car_model.lower().replace(' ', '-')}/"
        
        print(f"Starting scrape for car model: {car_model}")
        print(f"Search URL: {search_url}")
        
        try:
            self.setup_driver()
            
            # Get all listing URLs
            listing_urls = self.get_listing_urls(search_url)
            print(f"Found {len(listing_urls)} total listings")
            
            # Parse each listing
            listings = []
            for i, url in enumerate(listing_urls, 1):
                print(f"Parsing listing {i}/{len(listing_urls)}: {url}")
                listing_data = self.parse_listing_page(url)
                if listing_data:
                    listings.append(listing_data)
                time.sleep(self.config.DELAY_BETWEEN_REQUESTS)
                
            return listings
            
        finally:
            self.close_driver()
            
    def save_listings_to_db(self, listings: List[Dict]):
        """Save listings to database"""
        db = next(get_db())
        try:
            for listing_data in listings:
                # Check if listing already exists
                existing = db.query(CarListing).filter_by(olx_id=listing_data['olx_id']).first()
                
                if existing:
                    # Update existing listing
                    for key, value in listing_data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                    existing.updated_at = datetime.utcnow()
                else:
                    # Create new listing
                    car_listing = CarListing(**listing_data)
                    db.add(car_listing)
                    
            db.commit()
            print(f"Saved {len(listings)} listings to database")
            
        except Exception as e:
            db.rollback()
            print(f"Error saving to database: {e}")
        finally:
            db.close() 