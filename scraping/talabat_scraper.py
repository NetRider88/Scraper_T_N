# scraping/talabat_scraper.py

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .area_data import get_area_info

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_talabat(area, max_pages=26):
    """
    Scrape restaurant names and offers from Talabat UAE based on the area.

    Args:
        area (str): The area name to search for (e.g., 'kalba').
        max_pages (int, optional): Maximum number of pages to scrape. If None, scrape all pages.

    Returns:
        list: List of dictionaries with restaurant data.
    """
    # Get area information
    area_info = get_area_info(area)
    
    if not area_info['is_valid']:
        logging.error(f"Invalid area: {area}")
        return []
        
    area_code = area_info['talabat_code']
    if not area_code:
        logging.error(f"No Talabat code found for area: {area}")
        return []
        
    restaurants = []
    base_url = f"https://www.talabat.com/uae/restaurants/{area_code}/{area_info['key']}"
    
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 20)
        
        # Iterate through all pages directly
        for page in range(1, max_pages + 1):
            current_url = f"{base_url}?page={page}"
            logging.info(f"Scraping page {page} of {max_pages}: {current_url}")
            
            driver.get(current_url)
            time.sleep(3)  # Wait for page load
            
            try:
                # Wait for restaurants to load
                restaurant_selector = ".fFuryH .vendor-card"
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, restaurant_selector)))
                
                # Get all restaurant elements
                restaurant_elements = driver.find_elements(By.CSS_SELECTOR, restaurant_selector)
                
                # If no restaurants found, we might have reached the end
                if not restaurant_elements:
                    logging.info(f"No restaurants found on page {page}, might be the last page")
                    break
                
                logging.info(f"Found {len(restaurant_elements)} restaurants on page {page}")
                
                for element in restaurant_elements:
                    try:
                        name = element.find_element(By.CSS_SELECTOR, ".content h2").text
                        try:
                            offer = element.find_element(By.CSS_SELECTOR, ".offer-text").text
                        except:
                            offer = "No Offer"
                            
                        restaurants.append({
                            'name': name,
                            'offer': offer,
                            'platform': 'Talabat',
                            'page': page
                        })
                        logging.info(f"Scraped restaurant: {name} with offer: {offer}")
                        
                    except Exception as e:
                        logging.warning(f"Error processing restaurant: {e}")
                        continue
                
            except Exception as e:
                logging.error(f"Error on page {page}: {e}")
                continue
            
        driver.quit()
        logging.info(f"Total restaurants scraped: {len(restaurants)}")
        
    except Exception as e:
        logging.error(f"Error scraping Talabat: {e}")
        if 'driver' in locals():
            driver.quit()
    
    return restaurants
