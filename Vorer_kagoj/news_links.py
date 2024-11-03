# ittefaq_tcb_link_collector.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

import time, json
import random

user_agents = [
    "U-A: 1",
    "U-A: 2",
    "U-A: 3",
    "U-A: 4",
    "U-A: 5",
]

# Function to scrape the given URLs and save the output links to a JSON file
def scrape_links(output_file_name, urls_to_scrape):
    # Configure ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    time.sleep(random.uniform(1,3)) 
    
    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling
    
    #fetching news-type
    def get_news_type(url):
        if 'government' in url:
            return ['natonal', 'government']
        elif 'law-justice' in url:
            return ['national', 'law-justice']
        elif 'media' in url:
            return ['national', 'media']
        elif 'accident' in url:
            return ['national', 'accident']
        elif 'mourning' in url:
            return ['national', 'mourning']
        elif 'weather' in url:
            return ['national', 'weather']
        elif 'national-other' in url:
            return ['national','national-other']
        elif 'country' in url:
            return ['national', 'whole-country']
        
        elif 'crime' in url:
            return ['crime', 'general']
        
        elif 'awamileague' in url:
            return ['politics', 'awamileague']
        elif 'bnp' in url:
            return ['politics', 'bnp']
        elif 'jp' in url:
            return ['politics', 'jp']
        elif 'jamat' in url:
            return ['politics', 'jamat']
        elif 'politics-other' in url:
            return ['politics', 'politics-other']
        elif 'worldtrade' in url:
            return ['economics', 'worldtrade']
        
        # International categories
        elif 'australia' in url:
            return ['international', 'australia']
        elif 'middleeast' in url:
            return ['international', 'middleeast']
        elif 'india' in url:
            return ['international', 'india']
        elif 'pakistan' in url:
            return ['international', 'pakistan']
        elif 'asia' in url:
            return ['international', 'asia']
        elif 'africa' in url:
            return ['international', 'africa']
        elif 'europe' in url:
            return ['international', 'europe']
        elif 'united-state' in url:
            return ['international', 'united-states']
        elif 'south-america' in url:
            return ['international', 'south-america']
        elif 'united-kingdom' in url:
            return ['international', 'united-kingdom']
        elif 'malaysia' in url:
            return ['international', 'malaysia']
        elif 'russia' in url:
            return ['international', 'russia']
        elif 'international-other' in url:
            return ['international', 'international-other']
        
        
        elif 'worldtrade' in url:
            return ['economics', 'worldtrade']
        elif 'corporate' in url:
            return ['economics', 'corporate']
        elif 'budget' in url:
            return ['economics', 'budget']
        elif 'export-import' in url:
            return ['economics', 'export-import']
        elif 'clothing' in url:
            return ['economics', 'clothing']
        elif 'share-market' in url:
            return ['economics', 'share-market']
        elif 'bank' in url:
            return ['economics', 'bank']
        elif 'insurance' in url:
            return ['economics', 'insurance']
        elif 'tourism' in url:
            return ['economics', 'tourism']
        elif 'revenue' in url:
            return ['economics', 'revenue']
        elif 'entrepreneur' in url:
            return ['economics', 'entrepreneur']
        elif 'private-org' in url:
            return ['economics', 'private-organization']
        elif 'economics-other' in url:
            return ['economics', 'economics-other']
        elif 'north-america' in url:
            return ['economics', 'north-america']
        elif 'business' in url:
            return ['economics', 'business']
            
        # Sports categories
        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'tennis' in url:
            return ['sports', 'tennis']
        elif 'hockey' in url:
            return ['sports', 'hockey']
        elif 'sports-interview' in url:
            return ['sports', 'interview']
        elif 'bpl' in url:
            return ['sports', 'bpl']
        elif 'ipl' in url:
            return ['sports', 'ipl']
        elif 'sports-other' in url:
            return ['sports', 'sports-other']
        
        # Entertainment categories
        elif 'dhallywood' in url:
            return ['entertainment', 'dhallywood']
        elif 'bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'tallywood' in url:
            return ['entertainment', 'tallywood']
        elif 'hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'drama' in url:
            return ['entertainment', 'drama']
        elif 'music' in url:
            return ['entertainment', 'music']
        elif 'entertainment-interview' in url:
            return ['entertainment', 'interview']
        elif 'entertainment-other' in url:
            return ['entertainment', 'other']
        
        elif 'makeup' in url:
            return ['lifestyle', 'makeup']
        elif 'home-decoration' in url:
            return ['lifestyle', 'home-decoration']
        elif 'fashion' in url:
            return ['lifestyle', 'fashion']
        elif 'tips' in url:
            return ['lifestyle', 'tips']
        elif 'solution' in url:
            return ['lifestyle', 'solution']
        elif 'food' in url:
            return ['lifestyle', 'food']
        elif 'lifestyle-other' in url:
            return ['lifestyle', 'other']
        
        elif 'admission' in url:
            return ['education', 'admission']
        elif 'exam' in url:
            return ['education', 'exam']
        elif 'result' in url:
            return ['education', 'result']
        elif 'scholarship' in url:
            return ['education', 'scholarship']
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'study-abroad' in url:
            return ['education', 'study-abroad']
        elif 'tutorial-other' in url:
            return ['education', 'other']

        elif 'tech-news' in url:
            return ['technology', 'tech-news']
        elif 'telecom' in url:
            return ['technology', 'telecom']
        elif 'mobile' in url:
            return ['technology', 'mobile']
        elif 'tech-socialmedia' in url:
            return ['technology', 'socialmedia']
        elif 'tech-apps' in url:
            return ['technology', 'apps']
        elif 'innovation' in url:
            return ['technology', 'innovation']
        elif 'freelancing' in url:
            return ['technology', 'freelancing']
        elif 'review' in url:
            return ['technology', 'review']
        elif 'tech-interview' in url:
            return ['technology', 'interview']
        elif 'tech-other' in url:
            return ['technology', 'other']
        
        elif 'opinion' in url:
            return ['opinion', 'general']
        
        elif 'health' in url:
            return ['health', 'general']

        elif 'science' in url:
            return ['science', 'general']

        elif '/lifestyle-travel' in url:
            return ['travel', 'general']
        elif '/travel' in url:
            return ['travel', 'general']
        
        elif 'probas' in url:
            return ['expatriate', 'general']
        
        elif 'prose' in url:
            return ['literature', 'prose']
        elif 'story' in url:
            return ['literature', 'story']
        elif 'poem' in url:
            return ['literature', 'poem']
        elif 'literature-interview' in url:
            return ['literature', 'interview']
        elif 'bookfair' in url:
            return ['literature', 'bookfair']
        elif 'book-discussion' in url:
            return ['literature', 'book-discussion']
        elif 'literature-other' in url:
            return ['literature', 'other']



        
                
            
            
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
        time.sleep(random.uniform(1,3)) 
        links = set()  # Use a set to avoid duplicates
        
        card_elements_1 = driver.find_elements(By.CSS_SELECTOR, 'div.col-sm-4.col-md-4.paddingLR10.desktopSectionLead > div.thumbnail.marginB15 > a')
        card_elements_2 = driver.find_elements(By.CSS_SELECTOR, 'div.col-sm-8.col-md-8.paddingLR10.desktopSectionLead > div.thumbnail > a')
        card_elements_3 = driver.find_elements(By.CSS_SELECTOR, 'div.col-sm-12.col-md-12.lastItemNone > div.desktopSectionLead.marginB15 > div.thumbnail.borderRadius0.bgUnset.borderC1B1 > a')
        # card_elements_4 = driver.find_elements(By.CSS_SELECTOR, 'div.col-lg-4.d-flex > div.DInternationalList.align-self-stretch > a')
        card_elements = card_elements_1 + card_elements_2 + card_elements_3
        
        
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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div > a")))

        # Step 1: Click all "See More" buttons
        click_see_more_button()

        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        try:
            news_types = get_news_type(url)
            news_type = news_types[0]
            news_subcategory = news_types[1]
        except:
            news_type = None
            news_subcategory = None
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
        # 'https://www.bhorerkagoj.com/government',
        # 'https://www.bhorerkagoj.com/law-justice',
        # 'https://www.bhorerkagoj.com/media',
        # 'https://www.bhorerkagoj.com/accident',
        # 'https://www.bhorerkagoj.com/mourning',
        # 'https://www.bhorerkagoj.com/weather',
        # 'https://www.bhorerkagoj.com/national-other',
        #  'https://www.bhorerkagoj.com/country',
        
        # 'https://www.bhorerkagoj.com/crime',
        
        # 'https://www.bhorerkagoj.com/awamileague',
        # 'https://www.bhorerkagoj.com/bnp',
        # 'https://www.bhorerkagoj.com/jp',
        # 'https://www.bhorerkagoj.com/jamat',
        # 'https://www.bhorerkagoj.com/politics-other',

        'https://www.bhorerkagoj.com/australia',
        'https://www.bhorerkagoj.com/middleeast',
        'https://www.bhorerkagoj.com/india',
        'https://www.bhorerkagoj.com/pakistan',
        'https://www.bhorerkagoj.com/asia',
        'https://www.bhorerkagoj.com/africa',
        'https://www.bhorerkagoj.com/europe',
        'https://www.bhorerkagoj.com/united-state',
        'https://www.bhorerkagoj.com/south-america',
        'https://www.bhorerkagoj.com/united-kingdom',
        'https://www.bhorerkagoj.com/malaysia',
        'https://www.bhorerkagoj.com/russia',
        'https://www.bhorerkagoj.com/international-other',

        'https://www.bhorerkagoj.com/worldtrade',
        'https://www.bhorerkagoj.com/corporate',
        'https://www.bhorerkagoj.com/budget',
        'https://www.bhorerkagoj.com/export-import',
        'https://www.bhorerkagoj.com/clothing',
        'https://www.bhorerkagoj.com/share-market',
        'https://www.bhorerkagoj.com/bank',
        'https://www.bhorerkagoj.com/insurance',
        'https://www.bhorerkagoj.com/tourism',
        'https://www.bhorerkagoj.com/revenue',
        'https://www.bhorerkagoj.com/entrepreneur',
        'https://www.bhorerkagoj.com/private-org',
        'https://www.bhorerkagoj.com/economics-other',
        'https://www.bhorerkagoj.com/north-america',
        'https://www.bhorerkagoj.com/business',

        'https://www.bhorerkagoj.com/cricket',
        'https://www.bhorerkagoj.com/football',
        'https://www.bhorerkagoj.com/tennis',
        'https://www.bhorerkagoj.com/hockey',
        'https://www.bhorerkagoj.com/sports-interview',
        'https://www.bhorerkagoj.com/bpl',
        'https://www.bhorerkagoj.com/ipl',
        'https://www.bhorerkagoj.com/sports-other',

        'https://www.bhorerkagoj.com/dhallywood',
        'https://www.bhorerkagoj.com/bollywood',
        'https://www.bhorerkagoj.com/tallywood',
        'https://www.bhorerkagoj.com/hollywood',
        'https://www.bhorerkagoj.com/drama',
        'https://www.bhorerkagoj.com/music',
        'https://www.bhorerkagoj.com/entertainment-interview',
        'https://www.bhorerkagoj.com/entertainment-other',

        'https://www.bhorerkagoj.com/makeup',
        'https://www.bhorerkagoj.com/home-decoration',
        'https://www.bhorerkagoj.com/fashion',
        'https://www.bhorerkagoj.com/tips',
        'https://www.bhorerkagoj.com/solution',
        'https://www.bhorerkagoj.com/food',
        'https://www.bhorerkagoj.com/lifestyle-other',
        
        'https://www.bhorerkagoj.com/admission',
        'https://www.bhorerkagoj.com/exam',
        'https://www.bhorerkagoj.com/result',
        'https://www.bhorerkagoj.com/scholarship',
        'https://www.bhorerkagoj.com/campus',
        'https://www.bhorerkagoj.com/study-abroad',
        'https://www.bhorerkagoj.com/tutorial-other',

        'https://www.bhorerkagoj.com/tech-news',
        'https://www.bhorerkagoj.com/telecom',
        'https://www.bhorerkagoj.com/mobile',
        'https://www.bhorerkagoj.com/tech-socialmedia',
        'https://www.bhorerkagoj.com/tech-apps',
        'https://www.bhorerkagoj.com/innovation',
        'https://www.bhorerkagoj.com/freelancing',
        'https://www.bhorerkagoj.com/review',
        'https://www.bhorerkagoj.com/tech-interview',
        'https://www.bhorerkagoj.com/tech-other',

        'https://www.bhorerkagoj.com/opinion',

        'https://www.bhorerkagoj.com/health',

        'https://www.bhorerkagoj.com/science',
        
        'https://www.bhorerkagoj.com/lifestyle-travel',
        'https://www.bhorerkagoj.com/travel',

        'https://www.bhorerkagoj.com/prose',
        'https://www.bhorerkagoj.com/story',
        'https://www.bhorerkagoj.com/poem',
        'https://www.bhorerkagoj.com/literature-interview',
        'https://www.bhorerkagoj.com/bookfair',
        'https://www.bhorerkagoj.com/book-discussion',
        'https://www.bhorerkagoj.com/literature-other',

        'https://www.bhorerkagoj.com/probas',

    ]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Vorer_kagoj\\news_links.json", start_urls)
