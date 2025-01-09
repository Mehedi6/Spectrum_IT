# ittefaq_tcb_link_collector.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time, json
import html
import urllib.parse

# Function to scrape the given URLs and save the output links to a JSON file
def scrape_links(output_file_name, urls_to_scrape):
    # Configure ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)


    def get_news_type(url):
        if 'national' in url:
            return ['national', 'general']
        elif 'Court' in url:
            return ['national', 'law-&-justice']
        elif 'dhaka' in url:
            return ['national', 'capital']
        elif 'country-news' in url:
            return ['national', 'general']
        elif 'Politics' in url:
            return ['politics','general']
        
        elif 'world' in url:
            return ['international', 'agriculture-nature']
        elif 'sport' in url:
            return ['sports', 'general']
        elif 'entertainment' in url:
            return ['entertainment', 'general']
        elif 'stock-market' in url:
            return ['economics', 'stock-market']
        elif 'business' in url:
            return ['economics', 'business']
        elif 'campus-online' in url:
            return ['education', 'campus']
        elif 'science' in url:
            return ['science', 'general'] 
        elif 'jobs' in url:
            return ['jobs', 'general']
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        elif 'doctor-asen' in url:
            return ['health', 'general']
        elif 'chakriache' in url:
            return ['jobs', 'available_job']
        elif 'silalipi' in url:
            return ['literature', 'general']
        elif 'rongermela' in url:
            return ['entertainment', 'others']
        elif 'profit-loss' in url:
            return ['economy', 'profit-loss']
        elif 'eid-utshob2024' in url:
            return ['lifestyle', 'eid-cooking']
        
        
        
        
        
        
    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling
    
    
    # Click the "See More" button until it no longer appears
    def click_see_more_button():
        while True:
            try:
                # Scroll down first to ensure the "See More" button is visible
                scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[6]/div/div[1]/div[3]/div[15]/div/a')    
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
        
        # card_elements_1 = driver.find_elements(By.CSS_SELECTOR, 'div.cat-2nd-lead > a')
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'div > div.col-12.col-md-12.col-lg-8.col-xl-8 > a')  
        # card_elements = card_elements_1 + card_elements_2

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

        url = urllib.parse.unquote(url)
        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()

        news_types = get_news_type(url)
        try:
            news_subcategory = news_types[1]
            news_type = news_types[0]
        except:
            news_subcategory = None
            news_type = None
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
    
    print(f"Saved {len(unique_links)} unique links to {output_file_name}")
    
    # Close the browser when done
    driver.quit()

# Example usage:
urls = [
    'https://www.kalerkantho.com/online/national',
    'https://www.kalerkantho.com/online/country-news',
    'https://www.kalerkantho.com/online/dhaka',
    'https://www.kalerkantho.com/online/Court',
    'https://www.kalerkantho.com/online/Politics',
    'https://www.kalerkantho.com/online/campus-online',
    'https://www.kalerkantho.com/online/world',
    'https://www.kalerkantho.com/online/sport',
    'https://www.kalerkantho.com/online/entertainment',
    'https://www.kalerkantho.com/online/business',
    'https://www.kalerkantho.com/online/lifestyle',
    'https://www.kalerkantho.com/online/stock-market',
    'https://www.kalerkantho.com/online/jobs',
    'https://www.kalerkantho.com/online/science',
    'https://www.kalerkantho.com/feature/doctor-asen',
    'https://www.kalerkantho.com/feature/chakriache',
    'https://www.kalerkantho.com/feature/silalipi',
    'https://www.kalerkantho.com/feature/rongermela',
    'https://www.kalerkantho.com/feature/profit-loss',
    'https://www.kalerkantho.com/feature/eid-utshob2024',
    
]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Kalerkantho\\news_links.json", urls)
