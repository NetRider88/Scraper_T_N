# test_talabat_scraper.py

from scraping.talabat_scraper import scrape_talabat
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_scrape_talabat():
    # Test with both hyphenated and underscore versions
    areas_to_test = ['al-faseel', 'al_faseel', 'faseel']
    
    for area in areas_to_test:
        logging.info(f"\nTesting area: {area}")
        try:
            restaurants = scrape_talabat(area)
            
            if not restaurants:
                logging.warning(f"No restaurants found for area: {area}")
                continue
                
            # Print results by page
            pages = {}
            for restaurant in restaurants:
                page_num = restaurant.get('page', 1)  # Default to page 1 if not specified
                if page_num not in pages:
                    pages[page_num] = []
                pages[page_num].append(restaurant)
            
            for page_num, page_restaurants in pages.items():
                logging.info(f"Page {page_num}: Found {len(page_restaurants)} restaurants")
                for restaurant in page_restaurants:
                    logging.info(f"- {restaurant['name']}: {restaurant['offer']}")
                    
        except Exception as e:
            logging.error(f"Error testing area '{area}': {str(e)}")

if __name__ == "__main__":
    test_scrape_talabat()
