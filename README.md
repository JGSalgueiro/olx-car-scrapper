# OLX Car Scraper

A Python-based web scraper for extracting car listings from OLX.pt and storing them in a database for analysis.

## Features

- **Web Scraping**: Extracts car listings from OLX.pt using Selenium
- **Database Storage**: Stores listings in SQLite database with SQLAlchemy ORM
- **Data Analysis**: Built-in utilities for analyzing scraped data
- **Export Capabilities**: Export data to CSV format
- **Anti-Detection**: Uses rotating user agents and delays to avoid blocking
- **Flexible Search**: Search for any car model using the URL pattern

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd olx-auto-scrapper
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Chrome/Chromium** (required for Selenium):
   - Windows: Download from https://www.google.com/chrome/
   - Linux: `sudo apt-get install chromium-browser`
   - macOS: `brew install --cask google-chrome`

## Quick Start

1. **Initialize the database**:
```bash
python main.py --init-db
```

2. **Scrape car listings**:
```bash
python main.py --car-model "lancia-delta-hf"
```

3. **Run the example script**:
```bash
python example_usage.py
```

## Usage

### Command Line Interface

```bash
# Initialize database
python main.py --init-db

# Scrape specific car model
python main.py --car-model "bmw-e30" --max-pages 5

# Scrape with custom page limit
python main.py --car-model "mercedes-190e" --max-pages 20
```

### Python API

```python
from models import create_tables
from scraper import OLXScraper
from database_utils import export_to_csv

# Initialize database
create_tables()

# Create scraper
scraper = OLXScraper()

# Scrape listings
listings = scraper.scrape_car_model("lancia-delta-hf")

# Save to database
scraper.save_listings_to_db(listings)

# Export to CSV
export_to_csv("lancia_delta.csv", "lancia delta")
```

### Database Analysis

```python
from database_utils import get_listings_summary, get_price_analysis

# Get summary statistics
summary = get_listings_summary()
print(f"Total listings: {summary['total_listings']}")

# Get price analysis for specific model
price_analysis = get_price_analysis("bmw")
if price_analysis:
    print(f"Average price: €{price_analysis['average']:,.0f}")
```

## Configuration

Edit `config.py` to customize scraping behavior:

```python
class Config:
    # Database settings
    DATABASE_URL = 'sqlite:///olx_cars.db'
    
    # Scraping settings
    DELAY_BETWEEN_REQUESTS = 2  # seconds
    MAX_PAGES = 10  # maximum pages per search
    
    # Selenium settings
    SELENIUM_TIMEOUT = 10
    SELENIUM_IMPLICIT_WAIT = 5
```

## Database Schema

The scraper stores the following information for each listing:

- **Basic Info**: Title, price, currency, location, URL
- **Car Details**: Brand, model, year, mileage, fuel type, transmission
- **Seller Info**: Seller name, seller type
- **Metadata**: Creation date, update date, active status
- **Images**: JSON array of image URLs

## URL Pattern

The scraper uses the OLX URL pattern:
```
https://www.olx.pt/carros-motos-e-barcos/carros/q-{car-model}/
```

Examples:
- `https://www.olx.pt/carros-motos-e-barcos/carros/q-lancia-delta-hf/`
- `https://www.olx.pt/carros-motos-e-barcos/carros/q-bmw-e30/`
- `https://www.olx.pt/carros-motos-e-barcos/carros/q-mercedes-190e/`

## Data Analysis Features

### Summary Statistics
- Total and active listings count
- Price range and average price
- Recent listings (last 7 days)

### Export Options
- Export all listings to CSV
- Filter by car model
- Include all relevant fields

### Price Analysis
- Average, median, min, max prices
- Price distribution analysis
- Model-specific price trends

## Anti-Detection Measures

The scraper includes several features to avoid being blocked:

- **Rotating User Agents**: Uses fake-useragent library
- **Request Delays**: Configurable delays between requests
- **Headless Browser**: Runs Chrome in headless mode
- **Anti-Automation**: Disables automation detection flags

## Error Handling

The scraper handles various error scenarios:

- Network timeouts and connection errors
- Missing or malformed data
- Database connection issues
- Selenium driver errors

## Legal Considerations

⚠️ **Important**: Web scraping may be subject to legal restrictions. Please:

1. Review OLX.pt's Terms of Service and robots.txt
2. Respect rate limits and be mindful of server load
3. Use scraped data responsibly and in compliance with applicable laws
4. Consider implementing additional delays for production use

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**:
   - The scraper automatically downloads ChromeDriver
   - Ensure Chrome/Chromium is installed

2. **No listings found**:
   - Check if the car model exists on OLX.pt
   - Verify the URL format is correct
   - Try different car model names

3. **Database errors**:
   - Ensure the database directory is writable
   - Run `python main.py --init-db` to recreate tables

4. **Selenium errors**:
   - Update Chrome to the latest version
   - Check if antivirus is blocking ChromeDriver

### Debug Mode

To run with more verbose output, modify the scraper to disable headless mode:

```python
# In scraper.py, comment out this line:
# chrome_options.add_argument("--headless")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with OLX.pt's terms of service and applicable laws when using this scraper.

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for ensuring their use complies with OLX.pt's terms of service and applicable laws. The authors are not responsible for any misuse of this tool. 