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
                    (By.XPATH, '//*[@id="app"]/div/div[3]/div[4]/div/div/div[3]/button/span/span[1]')
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
    def extract_links():
        links = set()  # Use a set to avoid duplicates across all pages
        
        # Type 1: Cards with 'container.mb-3.mb-md-6.container--fluid.grid-list-xs a.color-black'
        card_elements_type_1 = driver.find_elements(By.CSS_SELECTOR, "div > div.pa-0.col-sm-12.col-md-5.col-lg-4.col-5 > div > a")
        
        for card in card_elements_type_1:
            link = card.get_attribute('href')
            # Avoid specific unwanted links and add only unique ones to the set
            if link and link not in ["https://www.somoynews.tv/categories/%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF","https://www.somoynews.tv/categories/%E0%A6%AC%E0%A6%BE%E0%A6%A3%E0%A6%BF%E0%A6%9C%E0%A7%8D%E0%A6%AF","https://www.somoynews.tv/categories/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6"]:
                links.add(link)
        
        # Type 2: Cards with 'div.py-0.col-md-4.col-12 a.color-black'
        card_elements_type_2 = driver.find_elements(By.CSS_SELECTOR, "div.py-0.col-md-4.col-12 a.color-black")

        for card in card_elements_type_2:
            link = card.get_attribute('href')
            # Avoid specific unwanted links and add only unique ones to the set
            if link and link not in ["https://www.somoynews.tv/categories/%E0%A6%AC%E0%A6%A3%E0%A6%BF%E0%A6%9C%E0%A7%8D%E0%A6%AF", 
                                     "https://www.somoynews.tv/categories/%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF",
                                     "https://www.somoynews.tv/categories/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6"]:
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
scrape_links("C:\\Users\\arwen\\Desktop\\TCB\\ShomoyNews\\somoytv_tcb_unique_links.json", [
    "https://www.somoynews.tv/topic/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF"
    ])