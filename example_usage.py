#!/usr/bin/env python3
"""
Example usage of OLX Car Scraper
Demonstrates how to use the scraper for different car models
"""

from models import create_tables
from scraper import OLXScraper
from database_utils import get_listings_summary, export_to_csv, get_price_analysis
import time

def example_scrape_lancia_delta():
    """Example: Scrape Lancia Delta HF listings"""
    print("=== Example: Scraping Lancia Delta HF ===")
    
    scraper = OLXScraper()
    
    # Scrape listings
    listings = scraper.scrape_car_model("lancia-delta-hf")
    
    if listings:
        print(f"Found {len(listings)} Lancia Delta HF listings")
        
        # Save to database
        scraper.save_listings_to_db(listings)
        
        # Get price analysis
        price_analysis = get_price_analysis("lancia delta")
        if price_analysis:
            print(f"Price Analysis:")
            print(f"  Average Price: €{price_analysis['average']:,.0f}")
            print(f"  Price Range: €{price_analysis['min']:,.0f} - €{price_analysis['max']:,.0f}")
        
        # Export to CSV
        export_to_csv("lancia_delta_listings.csv", "lancia delta")
    else:
        print("No Lancia Delta HF listings found")

def example_scrape_multiple_models():
    """Example: Scrape multiple car models"""
    car_models = [
        "bmw-e30",
        "mercedes-190e",
        "volkswagen-golf-gti"
    ]
    
    scraper = OLXScraper()
    
    for model in car_models:
        print(f"\n=== Scraping {model.upper()} ===")
        
        try:
            listings = scraper.scrape_car_model(model)
            
            if listings:
                print(f"Found {len(listings)} {model} listings")
                scraper.save_listings_to_db(listings)
            else:
                print(f"No {model} listings found")
                
            # Wait between models to be respectful
            time.sleep(5)
            
        except Exception as e:
            print(f"Error scraping {model}: {e}")

def example_database_analysis():
    """Example: Analyze scraped data"""
    print("\n=== Database Analysis ===")
    
    # Get summary
    summary = get_listings_summary()
    print(f"Total Listings: {summary['total_listings']}")
    print(f"Active Listings: {summary['active_listings']}")
    print(f"Average Price: €{summary['average_price']:,.0f}")
    print(f"Price Range: €{summary['min_price']:,.0f} - €{summary['max_price']:,.0f}")
    print(f"Recent Listings (7 days): {summary['recent_listings']}")
    
    # Export all data
    export_to_csv("all_listings.csv")

def main():
    """Main example function"""
    print("OLX Car Scraper - Example Usage")
    print("=" * 40)
    
    # Initialize database
    print("Initializing database...")
    create_tables()
    
    # Example 1: Scrape specific model
    example_scrape_lancia_delta()
    
    # Example 2: Scrape multiple models
    # Uncomment to run
    # example_scrape_multiple_models()
    
    # Example 3: Analyze data
    example_database_analysis()

if __name__ == "__main__":
    main() 