# scraping/noon_scraper.py

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
from .area_mapping import AreaMapping

def scrape_noon_food(area, max_pages=26):
    """
    Scrape restaurant names and offers from Noon Food based on the area.
    
    Args:
        area (str): The area name to search for
        max_pages (int): Maximum number of pages to scrape
    """
    # Initialize restaurants list at the start
    restaurants = []
    
    # Get area information using AreaMapping
    area_info = AreaMapping.get_area_info(area)
    if not area_info['is_valid']:
        logging.error(f"Invalid area: {area}")
        return []
        
    area_name = area_info['noon_name']
    if not area_name:
        logging.error(f"No Noon name found for area: {area}")
        return []
        
    logging.info(f"Searching for restaurants in: {area_name}")
    
    options = webdriver.FirefoxOptions()
    # Remove headless mode for testing
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 30)
        
        # Load the main page
        logging.info("Loading main page...")
        driver.get("https://food.noon.com/")
        time.sleep(5)
        
        # Find and interact with the search box
        search_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Search your location']")
        ))
        search_box.clear()
        search_box.send_keys(area_name)
        time.sleep(2)
        
        try:
            # Wait for suggestions container
            suggestions_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bJaVll")))
            
            # Find the first suggestion using the specific class
            first_suggestion = suggestions_container.find_element(By.CSS_SELECTOR, ".kinJyI")
            logging.info(f"Found first suggestion: {first_suggestion.text}")
            
            # Click the first suggestion
            driver.execute_script("arguments[0].click();", first_suggestion)
            time.sleep(2)
            
            # After location selection, wait for and click the "View Restaurants" button
            view_restaurants_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".jaMInw"))
            )
            logging.info("Clicking View Restaurants button")
            driver.execute_script("arguments[0].click();", view_restaurants_button)
            time.sleep(5)  # Wait for restaurants page to load
            
            # After clicking View Restaurants button and initial page load
            base_url = "https://food.noon.com/search/"
            
            # Now proceed with pagination and scraping
            for page in range(1, max_pages + 1):
                try:
                    if page > 1:
                        # Construct URL for pages 2 onwards
                        current_url = f"{base_url}?page={page}&type=outlet"
                        logging.info(f"Navigating to page {page}: {current_url}")
                        driver.get(current_url)
                        time.sleep(3)  # Wait for page load
                    
                    # Wait for restaurants to load
                    restaurant_selector = "a.drpCiq"
                    restaurants_present = wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, restaurant_selector))
                    )
                    
                    if not restaurants_present:
                        logging.info(f"No restaurants found on page {page}, might be the last page")
                        break
                    
                    logging.info(f"Found {len(restaurants_present)} restaurants on page {page}")
                    
                    # Scroll through the page to load all elements
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                    for element in restaurants_present:
                        try:
                            name = element.find_element(By.CSS_SELECTOR, "p.title").text
                            try:
                                offer = element.find_element(By.CSS_SELECTOR, "span.hBQSxC").text
                            except NoSuchElementException:
                                offer = "No Offer"
                                
                            restaurants.append({
                                'name': name,
                                'offer': offer,
                                'platform': 'Noon',
                                'page': page
                            })
                            logging.info(f"Scraped restaurant: {name} with offer: {offer}")
                            
                        except Exception as e:
                            logging.warning(f"Error processing restaurant: {str(e)}")
                            continue
                    
                except TimeoutException:
                    logging.error(f"Timeout waiting for restaurants to load on page {page}")
                    break
                except Exception as e:
                    logging.error(f"Error on page {page}: {str(e)}")
                    break
                    
        except Exception as e:
            logging.error(f"Error during area search: {str(e)}")
            
    except Exception as e:
        logging.error(f"Error scraping Noon: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("final_error.png")
    finally:
        if 'driver' in locals():
            driver.quit()
    
    return restaurants
