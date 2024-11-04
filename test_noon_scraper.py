# test_noon_scraper.py

from scraping.noon_scraper import scrape_noon_food
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Test with Kalba
area = "Kalba"
max_pages = 2  # Starting with 2 pages for initial test

try:
    print(f"\nStarting to scrape restaurants in {area}...")
    results = scrape_noon_food(area, max_pages)
    print(f"\nTotal restaurants found: {len(results)}")
    
    if results:
        print("\nFirst 5 restaurants:")
        for restaurant in results[:5]:
            print(f"Name: {restaurant['name']}")
            print(f"Offer: {restaurant['offer']}")
            print("---")
    else:
        print("No restaurants found.")
        
except Exception as e:
    print(f"Error during scraping: {str(e)}") 