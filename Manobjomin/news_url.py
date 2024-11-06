# ittefaq_tcb_link_collector.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time, json

# Function to scrape the given URLs and save the output links to a JSON file
def scrape_links(output_file_name, urls_to_scrape):
    # Configure ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    #News Types
    def get_news_type(url):
        if 'cat=4' in url:
            return ['sports', 'general']
        elif 'cat=5' in url:
            return ['international', 'general']
        elif 'cat=6' in url:
            return ['entertainment', 'general']
        elif 'cat=7' in url:
            return ['national-international', 'general'] 
        elif 'cat=8' in url:
            return ['national', 'general'] 
        elif 'cat=9' in url:
            return ['opinion', 'general'] 
        elif 'cat=10' in url:
            return ['education', 'general'] 
        elif 'cat=11' in url:
            return ['economics', 'general'] 
        elif 'cat=24' in url:
            return ['politics', 'general'] 
        elif 'cat=13' in url:
            return ['international', 'india'] 
        elif 'cat=15' in url:
            return ['technology', 'information-technology'] 
        
        elif 'cat=16' in url:
            return ['health', 'general'] 
        elif 'cat=23' in url:
            return ['expatriate', 'general'] 
        elif 'cat=12' in url:
            return ['international', 'india-kolkata'] 

    
    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for content to load after scrolling
    
    # Click the "See More" button until it no longer appears
    def click_see_more_button():
        while True:
            try:
                # Scroll down first to ensure the "See More" button is visible
                scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="ajax_load_more_687_btn"]')
                ))

                try:
                    # Attempt to click the button
                    see_more_button.click()
                    print("Clicked 'See More' button.")
                    time.sleep(2)  # Wait for more content to load
                except ElementClickInterceptedException:
                    # If click is intercepted, scroll a bit more and retry
                    print("Click intercepted, scrolling and retrying...")
                    scroll_down()
                    see_more_button.click()

            except (TimeoutException, NoSuchElementException):
                # If no more "See More" button is found, break the loop
                print("No more 'See More' button found.")
                break
    
    # Extract links from both types of card elements
    # Function to extract links from both types of card elements
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'div.col-sm-6 > div.row.d-flex.flex-sm-row.flex-row-reverse > div.col-sm-8.col-7 > h4 > a')

        print(len(card_elements))
        for card in card_elements:
            link = card.get_attribute('href')
            if link:
                links.add(link)

        return links  # Return the unique links as a set

    # Collect all unique links across all pages
    all_links = set()
    
    for url in urls_to_scrape:
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        # Step 1: Click all "See More" buttons
        # click_see_more_button()

        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        news_types = get_news_type(url)
        news_type = news_types[0]
        news_subcategory = news_types[1]
        # all_links.update(links_data)  # Update the set to ensure all links are unique
        for link in links_data:
            all_links.add((link, news_type, news_subcategory))
    unique_links = [{"url": link[0], "news_type": link[1], "news_subcategory": link[2]} for link in all_links]  # Convert the set to a list of dicts
    try:
        with open(output_file_name, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []  # Initialize empty if file doesn't exist

    # Extract only new URLs not already in the file
    existing_urls = {item['url'] for item in existing_data}
    filtered_new_data = [item for item in unique_links if item['url'] not in existing_urls]

    # Append new data to existing data and write back to JSON
    existing_data.extend(filtered_new_data)
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    driver.quit()

# Example usage:

start_urls = [
        
        'https://mzamin.com/category.php?cat=4#gsc.tab=0',
        'https://mzamin.com/category.php?cat=5#gsc.tab=0',
        'https://mzamin.com/category.php?cat=6#gsc.tab=0',
        'https://mzamin.com/category.php?cat=7#gsc.tab=0',
        'https://mzamin.com/category.php?cat=8#gsc.tab=0',
        'https://mzamin.com/category.php?cat=9#gsc.tab=0',
        'https://mzamin.com/category.php?cat=10#gsc.tab=0',
        'https://mzamin.com/category.php?cat=11#gsc.tab=0',
        'https://mzamin.com/category.php?cat=24',
        'https://mzamin.com/category.php?cat=13#gsc.tab=0',
        'https://mzamin.com/category.php?cat=15#gsc.tab=0',
        'https://mzamin.com/category.php?cat=16#gsc.tab=0',
        'https://mzamin.com/category.php?cat=23#gsc.tab=0',
        'https://mzamin.com/category.php?cat=12#gsc.tab=0',


        
        
        
    ]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Manobjomin\\news_links.json", start_urls)
