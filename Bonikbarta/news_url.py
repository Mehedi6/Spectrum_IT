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
        elif 'country' in url:
            return ['national', 'whole-country']
        elif 'environment' in url:
            return ['national', 'environment']
        
        elif 'politics' in url:
            return ['politics', 'general']
        
        elif 'immigrant' in url:
            return ['Expatriate', 'general']
        
        elif 'south-asia' in url:
            return ['international', 'south-asia']
        elif 'africa' in url:
            return ['international', 'africa']
        elif 'middle-east' in url:
            return ['international', 'middle-east']
        elif 'southeast-asia' in url:
            return ['international', 'southeast-asia']
        elif 'america' in url:
            return ['international', 'america']
        elif 'europe' in url:
            return ['international', 'europe']
        elif 'oceania' in url:
            return ['international', 'oceania']
        
        elif 'industry-commerce' in url:
            return ['economics', 'industry-commerce']
        elif 'corporate' in url:
            return ['economics', 'corporate']
        elif 'share-market' in url:
            return ['economics', 'share-market']
        elif 'bank' in url:
            return ['economics', 'bank']
        elif 'agriculture' in url:
            return ['economics', 'agriculture']
        elif 'international-business' in url:
            return ['economics', 'international-business']
        elif 'commodity-market' in url:
            return ['economics', 'commodity-market']
        elif 'analysis' in url:
            return ['economics', 'analysis']
        elif 'entrepreneur' in url:
            return ['economics', 'entrepreneur']
        
        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'tennis' in url:
            return ['sports', 'tennis']

        elif 'television' in url:
            return ['entertainment', 'television']
        elif 'ott' in url:
            return ['entertainment', 'ott']
        elif 'movie' in url:
            return ['entertainment', 'movie']
        elif 'song' in url:
            return ['entertainment', 'song']
        elif 'drama' in url:
            return ['entertainment', 'drama']
        elif 'talkies-interview' in url:
            return ['entertainment', 'interview']
        
        elif 'selfcare-beauty' in url:
            return ['lifestyle', 'selfcare-beauty']
        elif 'home-decoration' in url:
            return ['lifestyle', 'home-decoration']
        elif 'shopping' in url:
            return ['lifestyle', 'shopping']
        elif 'cooking' in url:
            return ['lifestyle', 'cooking']
        elif 'relationship' in url:
            return ['lifestyle', 'relationship']
        
        elif 'travel' in url:
            return ['travel', 'general']
        
        elif 'scitech' in url:
            return ['technology', 'science-technology']
        
        elif 'healthcare' in url:
            return ['health', 'general']

    
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
        
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'div.grow.group.relative.justify-between.gap-2.grid-cols-12.border-white > div > h3 > a')

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
        'https://bonikbarta.com/categories/national',
        'https://bonikbarta.com/categories/country',
        'https://bonikbarta.com/categories/environment',

        'https://bonikbarta.com/categories/politics',
        
        'https://bonikbarta.com/categories/immigrant',

        'https://bonikbarta.com/categories/south-asia',
        'https://bonikbarta.com/categories/africa',
        'https://bonikbarta.com/categories/middle-east',
        'https://bonikbarta.com/categories/southeast-asia',
        'https://bonikbarta.com/categories/america',
        'https://bonikbarta.com/categories/europe',
        'https://bonikbarta.com/categories/oceania',
        #Economics
        'https://bonikbarta.com/categories/industry-commerce',
        'https://bonikbarta.com/categories/corporate',
        'https://bonikbarta.com/categories/share-market',
        'https://bonikbarta.com/categories/bank',
        'https://bonikbarta.com/categories/agriculture',
        'https://bonikbarta.com/categories/international-business',
        'https://bonikbarta.com/categories/commodity-market',
        'https://bonikbarta.com/categories/analysis',
        'https://bonikbarta.com/categories/entrepreneur',

        'https://bonikbarta.com/categories/cricket',
        'https://bonikbarta.com/categories/football',
        'https://bonikbarta.com/categories/tennis',
        #Entertainment
        'https://bonikbarta.com/categories/television',
        'https://bonikbarta.com/categories/ott',
        'https://bonikbarta.com/categories/movie',
        'https://bonikbarta.com/categories/song',
        'https://bonikbarta.com/categories/drama',
        'https://bonikbarta.com/categories/talkies-interview',
        #Lifestye
        'https://bonikbarta.com/categories/selfcare-beauty',
        'https://bonikbarta.com/categories/home-decoration',
        'https://bonikbarta.com/categories/shopping',
        'https://bonikbarta.com/categories/cooking',
        'https://bonikbarta.com/categories/relationship',

        'https://bonikbarta.com/categories/travel',

        'https://bonikbarta.com/scitech',

        'https://bonikbarta.com/healthcare',
        
        
        
    ]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Bonikbarta\\news_links.json", start_urls)
