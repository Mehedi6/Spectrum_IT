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
        
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'div.title_holder > div > h2 > a')

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
        click_see_more_button()

        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        all_links.update(links_data)  # Update the set to ensure all links are unique
    
    # Step 3: Save the extracted unique links to a JSON file
    unique_links = [{"url": link} for link in all_links]  # Convert the set to a list of dicts
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(unique_links, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(unique_links)} unique links to {output_file_name}")
    
    # Close the browser when done
    driver.quit()

# Example usage:
scrape_links("ittefaq_tcb_unique_links.json", [
    "https://www.ittefaq.com.bd/topic/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF", 
    ])
