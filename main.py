#!/usr/bin/env python3
"""
OLX Car Scraper - Main Script
Scrapes car listings from OLX.pt and stores them in a database
"""

import sys
import argparse
from models import create_tables
from scraper import OLXScraper

def main():
    parser = argparse.ArgumentParser(description='OLX Car Scraper')
    parser.add_argument('--car-model', '-c', required=True, 
                       help='Car model to search for (e.g., "lancia-delta-hf")')
    parser.add_argument('--max-pages', '-p', type=int, default=10,
                       help='Maximum pages to scrape (default: 10)')
    parser.add_argument('--init-db', action='store_true',
                       help='Initialize database tables')
    
    args = parser.parse_args()
    
    # Initialize database if requested
    if args.init_db:
        print("Creating database tables...")
        create_tables()
        print("Database tables created successfully!")
        return
    
    # Initialize scraper
    scraper = OLXScraper()
    
    try:
        print(f"Starting OLX scraper for car model: {args.car_model}")
        
        # Scrape listings
        listings = scraper.scrape_car_model(args.car_model)
        
        if listings:
            print(f"Found {len(listings)} listings")
            
            # Save to database
            scraper.save_listings_to_db(listings)
            
            # Print summary
            print("\n=== SCRAPING SUMMARY ===")
            print(f"Car Model: {args.car_model}")
            print(f"Total Listings Found: {len(listings)}")
            
            if listings:
                prices = [l['price'] for l in listings if l['price']]
                if prices:
                    print(f"Price Range: €{min(prices):,.0f} - €{max(prices):,.0f}")
                    print(f"Average Price: €{sum(prices)/len(prices):,.0f}")
                
                locations = [l['location'] for l in listings if l['location']]
                if locations:
                    unique_locations = list(set(locations))
                    print(f"Locations: {', '.join(unique_locations[:5])}")
                    if len(unique_locations) > 5:
                        print(f"... and {len(unique_locations) - 5} more")
        else:
            print("No listings found for the specified car model.")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during scraping: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 