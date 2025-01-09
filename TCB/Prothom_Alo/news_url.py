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
                    (By.XPATH, '//div[@class="more _7ZpjE"]')  
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
        
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'div.card-with-image-zoom > h3 > a ')

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
        click_see_more_button()

        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        all_links.update(links_data)  # Update the set to ensure all links are unique
    
    # Step 3: Save the extracted unique links to a JSON file
    unique_links = [{"url": link} for link in all_links]  # Convert the set to a list of dicts
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

# Example usage:

start_urls = [
        
        #national
        # 'https://www.prothomalo.com/bangladesh',
        # 'https://www.prothomalo.com/bangladesh/capital',
        # 'https://www.prothomalo.com/bangladesh/district',
        # 'https://www.prothomalo.com/bangladesh/coronavirus',
        # 'https://www.prothomalo.com/bangladesh/environment',

        # #INTERNATIONAL
        # 'https://www.prothomalo.com/world',
        # 'https://www.prothomalo.com/collection/palestine-israel-conflict',
        # 'https://www.prothomalo.com/topic/রাশিয়া-ইউক্রেন-সংঘাত',
        # 'https://www.prothomalo.com/world/india',
        # 'https://www.prothomalo.com/world/pakistan',
        # 'https://www.prothomalo.com/world/china',
        # 'https://www.prothomalo.com/world/middle-east',
        # 'https://www.prothomalo.com/world/usa',
        # 'https://www.prothomalo.com/world/asia',
        # 'https://www.prothomalo.com/world/europe',
        # 'https://www.prothomalo.com/world/africa',
        # 'https://www.prothomalo.com/world/south-america',
        
        # #crime
        # 'https://www.prothomalo.com/bangladesh/crime',

        # 'https://www.prothomalo.com/business',
        # 'https://www.prothomalo.com/business/market',
        # 'https://www.prothomalo.com/business/bank',
        # 'https://www.prothomalo.com/business/industry',
        # 'https://www.prothomalo.com/business/economics',
        # 'https://www.prothomalo.com/business/world-business',
        # 'https://www.prothomalo.com/business/analysis',
        # 'https://www.prothomalo.com/business/personal-finance',
        # 'https://www.prothomalo.com/business/উদ্যোক্তা',
        # 'https://www.prothomalo.com/business/corporate',
        # 'https://www.prothomalo.com/collection/budget-2024-25',
    
        # 'https://www.prothomalo.com/opinion',
        # 'https://www.prothomalo.com/opinion/editorial',
        # 'https://www.prothomalo.com/opinion/column',
        # 'https://www.prothomalo.com/opinion/interview',
        # 'https://www.prothomalo.com/opinion/memoir',
        # 'https://www.prothomalo.com/opinion/reaction',
        # 'https://www.prothomalo.com/opinion/letter',
    
        # 'https://www.prothomalo.com/sports',
        # 'https://www.prothomalo.com/sports/cricket',
        # 'https://www.prothomalo.com/sports/football',
        # 'https://www.prothomalo.com/sports/tennis',
        # 'https://www.prothomalo.com/sports/other-sports',
        # 'https://www.prothomalo.com/sports/sports-interview',
        # 'https://www.prothomalo.com/collection/sports-photo-feature',
        # 'https://www.prothomalo.com/collection/sports-quiz',
        # 'https://www.prothomalo.com/collection/bangladesh-southafrica',
    
        # 'https://www.prothomalo.com/entertainment',
        # 'https://www.prothomalo.com/entertainment/tv',
        # 'https://www.prothomalo.com/entertainment/ott',
        # 'https://www.prothomalo.com/entertainment/dhallywood',
        # 'https://www.prothomalo.com/entertainment/tollywood',
        # 'https://www.prothomalo.com/entertainment/bollywood',
        # 'https://www.prothomalo.com/entertainment/hollywood',
        # 'https://www.prothomalo.com/entertainment/world-cinema',
        # 'https://www.prothomalo.com/entertainment/song',
        # 'https://www.prothomalo.com/entertainment/drama',
        # 'https://www.prothomalo.com/entertainment/entertainment-interview',
    
        # 'https://www.prothomalo.com/chakri',
        # 'https://www.prothomalo.com/chakri/chakri-news',
        # 'https://www.prothomalo.com/chakri/employment',
        # 'https://www.prothomalo.com/chakri/chakri-suggestion',
        # 'https://www.prothomalo.com/chakri/chakri-interview',
    
        # 'https://www.prothomalo.com/lifestyle',
        # 'https://www.prothomalo.com/lifestyle/relation',
        # 'https://www.prothomalo.com/lifestyle/horoscope',
        # 'https://www.prothomalo.com/lifestyle/fashion',
        # 'https://www.prothomalo.com/lifestyle/style',
        # 'https://www.prothomalo.com/lifestyle/beauty',
        # 'https://www.prothomalo.com/lifestyle/interior',
        # 'https://www.prothomalo.com/lifestyle/recipe',
        # 'https://www.prothomalo.com/lifestyle/shopping',

        # 'https://www.prothomalo.com/technology',
        # 'https://www.prothomalo.com/technology/gadget',
        # 'https://www.prothomalo.com/technology/advice',
        # 'https://www.prothomalo.com/technology/automobiles',
        # 'https://www.prothomalo.com/technology/cyberworld',
        # 'https://www.prothomalo.com/technology/freelancing',
        # 'https://www.prothomalo.com/technology/artificial-intelligence',

        # 'https://www.prothomalo.com/technology/science',

        # 'https://www.prothomalo.com/education',
        # 'https://www.prothomalo.com/education/admission',
        # 'https://www.prothomalo.com/education/examination',
        # 'https://www.prothomalo.com/education/scholarship',
        # 'https://www.prothomalo.com/education/study',
        # 'https://www.prothomalo.com/education/higher-education',
        # 'https://www.prothomalo.com/education/campus',

        # 'https://www.prothomalo.com/onnoalo',
        # 'https://www.prothomalo.com/onnoalo/poem',
        # 'https://www.prothomalo.com/onnoalo/stories',
        # 'https://www.prothomalo.com/onnoalo/treatise',
        # 'https://www.prothomalo.com/onnoalo/books',
        # 'https://www.prothomalo.com/onnoalo/arts',
        # 'https://www.prothomalo.com/onnoalo/interview',
        # 'https://www.prothomalo.com/onnoalo/travel',
        # 'https://www.prothomalo.com/onnoalo/others',
        # 'https://www.prothomalo.com/onnoalo/translation',
        # 'https://www.prothomalo.com/onnoalo/prose',
        # 'https://www.prothomalo.com/onnoalo/children',

        # 'https://www.prothomalo.com/lifestyle/health',

        # 'https://www.prothomalo.com/lifestyle/travel',

        'https://www.prothomalo.com/topic/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF',
    ]

scrape_links("C:\\Users\\arwen\\Desktop\\TCB\\Prothom_Alo\\prothom_alo_news_links.json", start_urls)