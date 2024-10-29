from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Initialize the driver
driver = webdriver.Chrome()
driver.get("https://www.somoynews.tv/categories/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6")
driver.maximize_window()

# List of sections to iterate over (adjust XPaths as needed)
sections = {
    'Dhaka': '//*[@id="app"]/div[1]/div[3]/div[5]/div/div/div/div/div[2]/div/div[2]',        # Placeholder XPaths for the buttons; adjust these by inspecting the page
    'Chattogram': '//*[@id="app"]/div[1]/div[3]/div[5]/div/div/div/div/div[2]/div/div[3]',
    # 'Khulna': '//*[@aria-label="Khulna Section"]',
    # 'Sylhet': '//*[@aria-label="Sylhet Section"]'
}

# Initialize dictionary to store results
news_links = {}

# Function to extract links from the current section
def extract_links():
    links = []
    try:
        # Wait until news items are loaded
        news_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/news/")]'))
        )
        # Extract links
        for element in news_elements:
            link = element.get_attribute('href')
            if link and link not in links:  # Avoid duplicates
                links.append(link)
    except Exception as e:
        print(f"Error extracting links: {e}")
    return links

# Iterate over each section
for section_name, xpath in sections.items():
    try:
        # Click on the section tab
        section_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        section_button.click()
        print(f"Clicked on {section_name} section")
        
        # Allow time for content to load
        time.sleep(2)

        # Extract and store the links for the section
        news_links[section_name] = extract_links()

    except Exception as e:
        print(f"Error with section {section_name}: {e}")

# Save results to JSON
with open("news_links.json", "w", encoding="utf-8") as f:
    json.dump(news_links, f, ensure_ascii=False, indent=4)

print("News links extraction completed.")
driver.quit()


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
        driver.execute_script("window.scrollTo(0, 60);")
        time.sleep(2)  # Wait for content to load after scrolling
    
    # Click the "See More" button until it no longer appears
    def click_see_more_button():
        while True:
            try:
                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div[3]/div[6]/div/div/div[3]/div/div[3]/button')
                ))

                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView();", see_more_button)

                try:
                    # Attempt to click the button
                    see_more_button.click()
                    print("Clicked 'See More' button.")
                    time.sleep(2)  # Wait for more content to load
                except ElementClickInterceptedException:
                    # If click is intercepted, scroll slightly upwards and retry
                    print("Click intercepted, adjusting scroll and retrying...")
                    driver.execute_script("window.scrollBy(0, -200);")  # Adjusts scroll to move any blocking overlay
                    time.sleep(1)  # Allow time for the overlay to clear
                    see_more_button.click()  # Retry clicking

            except (TimeoutException, NoSuchElementException):
                # If no more "See More" button is found, break the loop
                print("No more 'See More' button found.")
                break
    
    # Extract links from both types of card elements
    # Function to extract links from both types of card elements
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'div.container.mt-6.container--fluid.pa-0.ma-0.grid-list-xs > a')

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

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ShomoyNews\\news_data.json", [
    "https://www.somoynews.tv/categories/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6", 
    ])

