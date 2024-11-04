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
        if 'national' in url:
            return ['national', 'general']
        elif 'city-metropolis' in url:
            return ['national', 'city-metropolitans']
        elif 'law-and-justice' in url:
            return ['national', 'law-justice']
        elif 'environment' in url:
            return ['national', 'environment']
        elif 'wholecountry/dhaka' in url:
            return ['national', 'capital-city']
        elif 'wholecountry/chittagong' in url:
            return ['national', 'chittagong']
        elif 'wholecountry/rajshahi' in url:
            return ['national', 'rajshahi']
        elif 'wholecountry/khulna' in url:
            return ['national', 'khulna']
        elif 'wholecountry/barisal' in url:
            return ['national', 'barisal']
        elif 'wholecountry/sylhet' in url:
            return ['national', 'sylhet']
        elif 'wholecountry/rangpur' in url:
            return ['national', 'rangpur']
        elif 'wholecountry/mymensingh' in url:
            return ['national', 'mymensingh']
        
        elif 'politics' in url:
            return ['politics', 'general']
        elif 'international' in url:
            return ['international', 'general']
        elif 'sports' in url:
            return ['sports', 'general']
        elif 'economics' in url:
            return ['economics', 'general']
        elif 'share-' in url:
            return ['economics', 'share-market']
        elif 'entertainment' in url:
            return ['entertainment', 'general']
        elif 'information-technology' in url:
            return ['technology', 'information-technology']
        elif 'art-and-literature' in url:
            return ['literature', 'art-and-literature']
        elif 'health-' in url:
            return ['health', 'general']
        elif 'education' in url:
            return ['education', 'general']
        elif 'life-style' in url:
            return ['life-style', 'general']
        elif 'open-opinion' in url:
            return ['opinion', 'open-opinion']
    
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
        
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-7 > div.catsubMoremedianews.val_page_btm > div.sub-news > a, div.row > div.col-md-3 > div.common-lead-content.position-relative > a, div.row > div.col-md-4 > a, div.col-md-4 > div.common-lead-content.position-relative > a')

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
        
        #national     

        'https://www.jaijaidinbd.com/national',
        'https://www.jaijaidinbd.com/city-metropolis',
        'https://www.jaijaidinbd.com/wholecountry/dhaka',
        'https://www.jaijaidinbd.com/wholecountry/chittagong',
        'https://www.jaijaidinbd.com/wholecountry/rajshahi',
        'https://www.jaijaidinbd.com/wholecountry/khulna',
        'https://www.jaijaidinbd.com/wholecountry/barisal',
        'https://www.jaijaidinbd.com/wholecountry/sylhet',
        'https://www.jaijaidinbd.com/wholecountry/rangpur',
        'https://www.jaijaidinbd.com/wholecountry/mymensingh',
        'https://www.jaijaidinbd.com/law-and-justice',
        'https://www.jaijaidinbd.com/environment',

        'https://www.jaijaidinbd.com/politics',
        
        'https://www.jaijaidinbd.com/international',
        
        'https://www.jaijaidinbd.com/sports',
        
        'https://www.jaijaidinbd.com/economics',
        'https://www.jaijaidinbd.com/share-',
        
        'https://www.jaijaidinbd.com/entertainment',
        
        'https://www.jaijaidinbd.com/information-technology',
        
        'https://www.jaijaidinbd.com/art-and-literature',
        
        'https://www.jaijaidinbd.com/health-',
        
        'https://www.jaijaidinbd.com/education',
        
        'https://www.jaijaidinbd.com/life-style',
        
        'https://www.jaijaidinbd.com/open-opinion',
        
    ]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Jay-Jay-Din\\news_links.json", start_urls)
