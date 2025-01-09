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
    
    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for content to load after scrolling
    
    #fetching news-type
    def get_news_type(url):
        if 'national' in url:
            if 'capital' in url:
                return ['national', 'capital']
            else:
                return ['national', 'general']
        if 'bangladesh' in url:
            return ['national', 'whole-country']
        
        if 'weather' in url:
            return ['national', 'weather']
        if 'international' in url:
            if 'asia' in url:
                return ['international', 'asia']
            elif 'europe' in url:
                return ['international', 'europe']
            elif 'america' in url:
                return ['international', 'america']
            elif 'africa' in url:
                return ['international', 'africa']
            elif 'australia' in url:
                return ['international', 'australia']
            elif 'middle-east' in url:
                return ['international', 'middle-east']
            elif 'others' in url:
                return ['international', 'others']
        if 'politics' in url:
            return ['politics', 'general']
        if 'sports' in url:
            if 'cricket' in url:
                return ['sports', 'cricket']
            elif 'football' in url:
                return ['sports', 'football']
            elif 'others-sports' in url:
                return ['sports', 'other-sports']
            
        if 'entertainment' in url:
            if 'movies' in url:
                return ['entertainment', 'movies']
            elif 'drama' in url:
                return ['entertainment', 'drama']
            elif 'song' in url:
                return ['entertainment', 'song']
            elif 'interviewer' in url:
                return ['entertainment', 'interviewer']
            elif 'ott' in url:
                return ['entertainment', 'ott']
            elif 'others-entertainment' in url:
                return ['entertainment', 'other-entertainments']
        if 'economy' in url:
            if 'industry' in url:
                return ['economics', 'industry']
            elif 'revenue' in url:
                return ['economics', 'revenue']
            elif 'bank' in url:
                return ['economics', 'bank']
            elif 'corporate' in url:
                return ['economics', 'corporate']
            elif 'e-commerce' in url:
                return ['economics', 'e-commerce']
        if 'sharebazar' in url:
            return ['economics', 'stock-market']
        if 'lifestyle' in url:
            if 'fashion' in url:
                return ['lifestyle', 'fashion']
            elif 'women' in url:
                return ['lifestyle', 'women']
            elif 'recipe' in url:
                return ['lifestyle', 'recipe']
            elif 'others-lifestyle' in url:
                return ['lifestyle', 'other-lifestyles']
        if 'travel' in url:
            return ['travel', 'general']
        
        if 'opinion' in url:
            return ['opinion', 'general']
        if 'health' in url:
            return ['health', 'general']
        if 'education' in url:
            return ['education', 'general']
        if 'science-technology' in url:
            return ['technology', 'science-technology']
        if 'job' in url:
            return ['job', 'general']
        if 'literature' in url:
            return ['literature', 'general']
        if 'migration' in url:
            return ['expatriate', 'general']
            
            
            
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
        
        card_elements_1 = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-6.col-12 > div.DSubCategoryList.countclass > a')
        card_elements_2 = driver.find_elements(By.CSS_SELECTOR, 'div.row.read-more-container > div.col-lg-12.col-12.countclass > div.DCatNewsList3 > a')
        card_elements_3 = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-4.col-sm-12 > div.DNationalTop2 > div.DNationalList > a')
        card_elements_4 = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-4.d-flex > div.DInternationalList.align-self-stretch > a')
        card_elements = card_elements_1 + card_elements_2 + card_elements_3 + card_elements_4

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
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

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
    
    print(f"Saved {len(unique_links)} unique links to {output_file_name}")
    
    # Close the browser when done
    driver.quit()

# Example usage:

start_urls = [
        
        #national
        
        'https://www.dailyjanakantha.com/national/capital',
        'https://www.dailyjanakantha.com/bangladesh/',
        'https://www.dailyjanakantha.com/weather/',
        ''
        
        'https://www.dailyjanakantha.com/international/asia',
        'https://www.dailyjanakantha.com/international/europe/',
        'https://www.dailyjanakantha.com/international/america/',
        'https://www.dailyjanakantha.com/international/africa/',
        'https://www.dailyjanakantha.com/international/australia/',
        'https://www.dailyjanakantha.com/international/middle-east/',
        'https://www.dailyjanakantha.com/international/others/',
        
        'https://www.dailyjanakantha.com/politics/',

        'https://www.dailyjanakantha.com/sports/cricket',
        'https://www.dailyjanakantha.com/sports/football',
        'https://www.dailyjanakantha.com/sports/others-sports',

        'https://www.dailyjanakantha.com/entertainment/movies',
        'https://www.dailyjanakantha.com/entertainment/drama',
        'https://www.dailyjanakantha.com/entertainment/song',
        'https://www.dailyjanakantha.com/entertainment/interviewer',
        'https://www.dailyjanakantha.com/entertainment/ott',
        'https://www.dailyjanakantha.com/entertainment/others-entertainment',

        'https://www.dailyjanakantha.com/economy/industry',
        'https://www.dailyjanakantha.com/economy/revenue',
        'https://www.dailyjanakantha.com/economy/bank',
        'https://www.dailyjanakantha.com/economy/corporate',
        'https://www.dailyjanakantha.com/economy/e-commerce',
        'https://www.dailyjanakantha.com/sharebazar/',

        'https://www.dailyjanakantha.com/lifestyle/fashion',
        'https://www.dailyjanakantha.com/lifestyle/women',
        'https://www.dailyjanakantha.com/lifestyle/recipe',
        'https://www.dailyjanakantha.com/lifestyle/others-lifestyle',
        
        'https://www.dailyjanakantha.com/lifestyle/travel',

        'https://www.dailyjanakantha.com/opinion/',
        'https://www.dailyjanakantha.com/migration/',
        'https://www.dailyjanakantha.com/health/',
        'https://www.dailyjanakantha.com/education/',
        'https://www.dailyjanakantha.com/science-technology/',
        'https://www.dailyjanakantha.com/job/',
        'https://www.dailyjanakantha.com/literature/',

    ]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Jonokontho\\news_links.json", start_urls)
