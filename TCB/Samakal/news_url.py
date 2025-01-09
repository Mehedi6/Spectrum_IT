import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import random

# Function to scroll the page, click 'See More', and collect card links
def scrape_links(output_file, urls):
    # Set up undetected ChromeDriver
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")  # Open browser in fullscreen
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)

    if isinstance(urls, str):
        urls = [urls]

    all_links = []

    for url in urls:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        while True:
            try:
                # Randomized slow scrolling
                scroll_pause_time = random.uniform(3, 5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)

                # Wait for the "See More" button to become clickable
                see_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/div/div/div/div[2]/div[2]/a'))
                )

                # Move to the button to ensure it's in view
                driver.execute_script("arguments[0].scrollIntoView();", see_more_button)
                time.sleep(1)  # Small pause to ensure smooth scrolling

                # Click the button with retry logic
                for attempt in range(3):  # Retry up to 3 times
                    try:
                        ActionChains(driver).move_to_element(see_more_button).click(see_more_button).perform()
                        print("Clicked 'See More' button successfully.")
                        break  # Exit retry loop on success
                    except Exception as click_error:
                        print(f"Click attempt {attempt + 1} failed: {click_error}")
                        time.sleep(random.uniform(1, 2))  # Wait before retrying

                # Random pause after click to simulate human behavior
                time.sleep(random.uniform(5, 8))

            except Exception as e:
                print(f"No more 'See More' buttons found or an error occurred: {e}")
                break

        # Once all content is loaded, find all card elements and extract links
        cards = driver.find_elements(By.CLASS_NAME, "CatListNews")

        # Loop through all the cards and extract the href from the <a> tag
        for card in cards:
            try:
                link_element = card.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
                all_links.append({"url": link})
            except Exception as link_error:
                print(f"Error extracting link: {link_error}")
                continue  # Skip any card that doesn't contain a link

    # Save the collected links into a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_links, f, ensure_ascii=False, indent=4)

    # Print the collected links for reference
    print(json.dumps(all_links, ensure_ascii=False, indent=4))

    # Ensure proper closure of the browser
    try:
        driver.quit()
    except Exception as e:
        print(f"Error during browser closure: {e}")

# Example usage of the function
scrape_links("card_links.json", [
    "https://samakal.com/topic/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF%E0%A6%B0%20%E0%A6%AA%E0%A6%A3%E0%A7%8D%E0%A6%AF",
    "https://samakal.com/topic/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF"
])