# test_scrapers.py

from scraping.noon_scraper import scrape_noon_food
from scraping.talabat_scraper import scrape_talabat
import logging

def test_noon_scraper():
    area = "al-faseel"  # Updated to match the same area as Talabat
    print(f"Testing Noon Food scraper for area: {area}")
    
    # Add logging similar to Talabat test
    logging.info(f"Starting Noon scrape for area: {area}")
    
    noon_data = scrape_noon_food(area)
    
    # Print results by page (if pagination exists)
    pages = {}
    for restaurant in noon_data:
        page_num = restaurant.get('page', 1)  # Default to page 1 if not specified
        if page_num not in pages:
            pages[page_num] = []
        pages[page_num].append(restaurant)
    
    for page_num, page_restaurants in pages.items():
        logging.info(f"Page {page_num}: Found {len(page_restaurants)} restaurants")
        for restaurant in page_restaurants:
            logging.info(f"- {restaurant['name']}: {restaurant['offer']}")
    
    logging.info(f"Total Noon restaurants scraped: {len(noon_data)}")

def test_talabat_scraper():
    area = "faseel"  # Example area; adjust as needed
    print(f"Testing Talabat UAE scraper for area: {area}")
    talabat_data = scrape_talabat(area)
    print(f"Talabat UAE scraped {len(talabat_data)} restaurants.")
    for restaurant in talabat_data:
        print(f"Name: {restaurant['name']}, Offer: {restaurant['offer']}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_noon_scraper()
    print("\n" + "="*50 + "\n")
    test_talabat_scraper()
