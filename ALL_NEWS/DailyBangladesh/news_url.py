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

    def get_news_type(url):
        if 'national' in url:
            return ['national', 'general']
        elif 'country' in url:
            return ['national', 'all-country']
        elif 'law-and-court' in url:
            return ['national', 'law-and-court']
        elif 'capital' in url:
            return ['national', 'capital']
        elif 'crime' in url:
            return ['crime', 'general']
        elif 'bd-politics' in url:
            return ['politics', 'general']
        elif 'international' in url:
            return ['international', 'general']
        elif 'economy' in url:
            return ['economics', 'economy']
        elif 'market-rate' in url:
            return ['business', 'market-rate']
        elif 'information-technology' in url:
            return ['technology', 'general']
        elif 'cyber-space' in url:
            return ['technology', 'cyber']
        elif 'education' in url:
            return ['education', 'general']
        elif 'sub/deshi' in url:
            return ['entertainment', 'local']
        elif 'sub/foreign' in url:
            return ['entertainment', 'foreign']
        elif 'sports' in url:
            return ['sports', 'general']
        elif 'art-and-culture' in url:
            return ['literature', 'art-and-culture']
        elif 'health-and-medical' in url:
            return ['health', 'medical']
        elif 'science' in url:
            return ['science', 'general']
        elif 'tourism' in url:
            return ['travel', 'tourism']
        elif 'opinion' in url:
            return ['opinion', 'editorial']
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        elif 'exile-life' in url:
            return ['expatriate', 'general']
        elif 'job-corner' in url:
            return ['jobs', 'general']
        else:
            return ['others', 'general']
    
    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling
    
    # Click the "See More" button until it no longer appears
    def click_see_more_button():
        count = 0
        max_attempts = 5  # Limit the number of attempts to avoid an infinite loop

        while count < max_attempts:
            try:
                # Scroll down slightly to ensure visibility of the button
                scroll_down()

                # Wait for the button to become clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@class="btn btn-lg btn-block ButtonBG"]')
                ))

                # Use JavaScript to scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)

                # Wait for a short duration to handle animation or rendering issues
                time.sleep(1)

                # Attempt to click the button
                see_more_button.click()
                print(f"Clicked 'See More' button (Attempt {count + 1}).")
                count += 1

                # Allow some time for content to load
                time.sleep(2)

            except ElementClickInterceptedException:
                # Handle click interception
                print("Click intercepted. Adjusting view and retrying...")
                driver.execute_script("window.scrollBy(0, -100);")  # Scroll up slightly and retry
                time.sleep(1)

            except (TimeoutException, NoSuchElementException):
                # Exit the loop if the button is not found or is no longer clickable
                print("No 'See More' button found or it is no longer clickable.")
                break
    # Extract links from both types of card elements
    # Function to extract links from both types of card elements
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        paths = ['//div[@class="DCatNewsList align-self-stretch"]/a',
                 '//div[@class="DCatLeadTop"]/a',
                 '//div[@class="DCatTop2 align-self-stretch"]/a',
                 '//div[@class="DCatTop3tList align-self-stretch"]/a',
                 ]
        
        # Loop through each XPath and extract links
        for path in paths:
            try:
                card_elements = driver.find_elements(By.XPATH, path)
                print(f"Found {len(card_elements)} elements for path: {path}")

                for card in card_elements:
                    link = card.get_attribute('href')
                    if link:
                        links.add(link)  # Add link to the set to avoid duplicates
            except Exception as e:
                print(f"Error extracting links for path {path}: {e}")

        return links  # Return the unique links as a set

    for url in urls_to_scrape:
        all_links = set()
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        news_type, news_subcategory = get_news_type(url)
        click_see_more_button()
        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        for link in links_data:
            if link not in {item[0] for item in all_links}:  # Check if URL is not already in the set
                all_links.add((link, news_type, news_subcategory))
        

    
        # Step 3: Save the extracted unique links to a JSON file
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

        print(f"Saved {len(filtered_new_data)} unique links to {output_file_name}")
    
    # Close the browser when done
    driver.quit()


news_urls = [
    'https://www.daily-bangladesh.com/national',
    'https://www.daily-bangladesh.com/country',
    'https://www.daily-bangladesh.com/law-and-court',
    'https://www.daily-bangladesh.com/capital',
    
    'https://www.daily-bangladesh.com/crime',

    'https://www.daily-bangladesh.com/bd-politics',

    'https://www.daily-bangladesh.com/international',

    'https://www.daily-bangladesh.com/economy',
    'https://www.daily-bangladesh.com/market-rate',

    'https://www.daily-bangladesh.com/information-technology',
    'https://www.daily-bangladesh.com/cyber-space',

    'https://www.daily-bangladesh.com/education',

    'https://www.daily-bangladesh.com/sub/deshi',
    'https://www.daily-bangladesh.com/sub/foreign',
    
    'https://www.daily-bangladesh.com/sports',
    
    'https://www.daily-bangladesh.com/art-and-culture',

    'https://www.daily-bangladesh.com/health-and-medical',

    'https://www.daily-bangladesh.com/science',

    'https://www.daily-bangladesh.com/tourism',

    'https://www.daily-bangladesh.com/opinion',

    'https://www.daily-bangladesh.com/lifestyle',

    'https://www.daily-bangladesh.com/exile-life',

    'https://www.daily-bangladesh.com/job-corner',


]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DailyBangladesh\\news_links.json", news_urls)
