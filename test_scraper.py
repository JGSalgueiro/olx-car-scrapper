#!/usr/bin/env python3
"""
Test script for OLX Car Scraper
Verifies that all components work correctly
"""

import sys
import os
from models import create_tables, get_db, CarListing
from scraper import OLXScraper
from database_utils import get_listings_summary

def test_database():
    """Test database creation and basic operations"""
    print("Testing database operations...")
    
    try:
        # Create tables
        create_tables()
        print("✓ Database tables created successfully")
        
        # Test database connection
        db = next(get_db())
        count = db.query(CarListing).count()
        print(f"✓ Database connection successful (current listings: {count})")
        db.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_scraper_initialization():
    """Test scraper initialization"""
    print("Testing scraper initialization...")
    
    try:
        scraper = OLXScraper()
        print("✓ Scraper initialized successfully")
        
        # Test driver setup (without actually scraping)
        scraper.setup_driver()
        print("✓ WebDriver setup successful")
        scraper.close_driver()
        
        return True
        
    except Exception as e:
        print(f"✗ Scraper initialization failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    
    try:
        from config import Config
        config = Config()
        
        # Check required attributes
        required_attrs = ['BASE_URL', 'DELAY_BETWEEN_REQUESTS', 'MAX_PAGES']
        for attr in required_attrs:
            if hasattr(config, attr):
                print(f"✓ Config attribute '{attr}' found")
            else:
                print(f"✗ Config attribute '{attr}' missing")
                return False
                
        print("✓ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("Testing dependencies...")
    
    required_packages = [
        'selenium',
        'beautifulsoup4',
        'requests',
        'sqlalchemy',
        'pandas',
        'fake_useragent',
        'webdriver_manager'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed")
    return True

def run_all_tests():
    """Run all tests"""
    print("OLX Car Scraper - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_config),
        ("Database", test_database),
        ("Scraper Initialization", test_scraper_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! The scraper is ready to use.")
        return True
    else:
        print("✗ Some tests failed. Please fix the issues before using the scraper.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 