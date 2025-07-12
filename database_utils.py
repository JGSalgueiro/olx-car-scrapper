"""
Database utilities for OLX Car Scraper
Provides functions for querying and analyzing scraped data
"""

import pandas as pd
from sqlalchemy import text
from models import get_db, CarListing
from datetime import datetime, timedelta

def get_listings_summary():
    """Get summary statistics of all listings"""
    db = next(get_db())
    try:
        total_listings = db.query(CarListing).count()
        active_listings = db.query(CarListing).filter_by(is_active=True).count()
        
        # Price statistics
        price_stats = db.query(
            CarListing.price,
            CarListing.currency
        ).filter(CarListing.price.isnot(None)).all()
        
        if price_stats:
            prices = [p[0] for p in price_stats]
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
        else:
            avg_price = min_price = max_price = 0
            
        # Recent listings (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_listings = db.query(CarListing).filter(
            CarListing.created_at >= week_ago
        ).count()
        
        return {
            'total_listings': total_listings,
            'active_listings': active_listings,
            'average_price': avg_price,
            'min_price': min_price,
            'max_price': max_price,
            'recent_listings': recent_listings
        }
        
    finally:
        db.close()

def get_listings_by_model(car_model: str, limit: int = 50):
    """Get listings for a specific car model"""
    db = next(get_db())
    try:
        listings = db.query(CarListing).filter(
            CarListing.title.ilike(f'%{car_model}%')
        ).order_by(CarListing.created_at.desc()).limit(limit).all()
        
        return listings
        
    finally:
        db.close()

def get_price_analysis(car_model: str = None):
    """Get price analysis for listings"""
    db = next(get_db())
    try:
        query = db.query(CarListing).filter(CarListing.price.isnot(None))
        
        if car_model:
            query = query.filter(CarListing.title.ilike(f'%{car_model}%'))
            
        listings = query.all()
        
        if not listings:
            return None
            
        prices = [l.price for l in listings]
        
        return {
            'count': len(prices),
            'average': sum(prices) / len(prices),
            'median': sorted(prices)[len(prices)//2],
            'min': min(prices),
            'max': max(prices),
            'prices': prices
        }
        
    finally:
        db.close()

def export_to_csv(filename: str = None, car_model: str = None):
    """Export listings to CSV file"""
    db = next(get_db())
    try:
        query = db.query(CarListing)
        
        if car_model:
            query = query.filter(CarListing.title.ilike(f'%{car_model}%'))
            
        listings = query.all()
        
        if not listings:
            print("No listings to export")
            return
            
        # Convert to DataFrame
        data = []
        for listing in listings:
            data.append({
                'olx_id': listing.olx_id,
                'title': listing.title,
                'price': listing.price,
                'currency': listing.currency,
                'location': listing.location,
                'seller_name': listing.seller_name,
                'year': listing.year,
                'mileage': listing.mileage,
                'fuel_type': listing.fuel_type,
                'transmission': listing.transmission,
                'url': listing.url,
                'created_at': listing.created_at,
                'updated_at': listing.updated_at
            })
            
        df = pd.DataFrame(data)
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'olx_listings_{timestamp}.csv'
            
        df.to_csv(filename, index=False)
        print(f"Exported {len(data)} listings to {filename}")
        
    finally:
        db.close()

def get_top_sellers(limit: int = 10):
    """Get top sellers by number of listings"""
    db = next(get_db())
    try:
        result = db.query(
            CarListing.seller_name,
            db.func.count(CarListing.id).label('listing_count')
        ).filter(
            CarListing.seller_name.isnot(None)
        ).group_by(CarListing.seller_name).order_by(
            db.func.count(CarListing.id).desc()
        ).limit(limit).all()
        
        return result
        
    finally:
        db.close()

def get_location_stats():
    """Get statistics by location"""
    db = next(get_db())
    try:
        result = db.query(
            CarListing.location,
            db.func.count(CarListing.id).label('listing_count'),
            db.func.avg(CarListing.price).label('avg_price')
        ).filter(
            CarListing.location.isnot(None),
            CarListing.price.isnot(None)
        ).group_by(CarListing.location).order_by(
            db.func.count(CarListing.id).desc()
        ).all()
        
        return result
        
    finally:
        db.close()

def cleanup_old_listings(days_old: int = 30):
    """Remove listings older than specified days"""
    db = next(get_db())
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        old_listings = db.query(CarListing).filter(
            CarListing.updated_at < cutoff_date
        ).all()
        
        count = len(old_listings)
        for listing in old_listings:
            db.delete(listing)
            
        db.commit()
        print(f"Removed {count} old listings (older than {days_old} days)")
        
    except Exception as e:
        db.rollback()
        print(f"Error cleaning up old listings: {e}")
    finally:
        db.close() 