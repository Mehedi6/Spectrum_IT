# Function to scrape the given URLs and save the output links to a JSON file
def scrape_links(output_file_name, urls_to_scrape):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
    import time, json

    # Configure ChromeDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)


    def get_news_type(url):
        if 'national' in url:
            return ['national', 'general']
        elif 'international' in url:
            return ['international', 'general']
        elif 'all-bangladesh' in url:
            return ['national', 'all-bangladesh']
        elif 'politics' in url:
            return ['politics', 'general']
        elif 'economy' in url:
            return ['economics', 'general']
        elif 'sports' in url:
            return ['sports', 'general']
        elif 'entertainment' in url:
            return ['entertainment', 'general']
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'travel' in url:
            return ['travel', 'general']
        elif 'health' in url:
            return ['health', 'general']
        elif 'technology' in url:
            return ['technology', 'general']
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        elif 'art-and-literature' in url:
            return ['literature', 'art-literature']
        else:
            return ['others', 'general']
    
    # Scroll down the page a limited number of times
    def scroll_down_limited(limit):
        for _ in range(limit):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load after scrolling

    # Extract links from loaded content
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        # Find card elements containing news links
        card_elements = driver.find_elements(By.XPATH, '//section[@class="row"]/article//a[@class="story-title-link story-link"]')
        card_elements_1 = driver.find_elements(By.XPATH, '//section[@class="row"]/div/article//a[@class="story-title-link story-link"]')
        print(f"Found {len(card_elements)} card elements.")

        for card in card_elements:
            link = card.get_attribute('href')
            if link:
                links.add(link)
        for card in card_elements_1:
            link = card.get_attribute('href')
            if link:
                links.add(link)

        return links  # Return unique links

    # Collect all unique links across all pages
    
    for url in urls_to_scrape:
        all_links = set()
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        # Step 1: Scroll a limited number of times
        scroll_down_limited(limit=7)  # Limit to 10 scrolls
        news_type, news_subcategory = get_news_type(url)
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

        print(f"Saved {len(filtered_new_data)} new links to {output_file_name}")

    # Close the browser when done
    driver.quit()

# Example usage:
start_urls = [
    'https://jamuna.tv/news/category/national',
    'https://jamuna.tv/news/category/all-bangladesh',
    'https://jamuna.tv/news/category/politics',
    'https://jamuna.tv/news/category/economy',
    'https://jamuna.tv/news/category/international',
    'https://jamuna.tv/news/category/sports',
    'https://jamuna.tv/news/category/entertainment',
    'https://jamuna.tv/news/category/campus',
    'https://jamuna.tv/news/category/travel',
    'https://jamuna.tv/news/category/health',
    'https://jamuna.tv/news/category/technology',
    'https://jamuna.tv/news/category/lifestyle',
    'https://jamuna.tv/news/category/art-and-literature',

]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Jamuna_TV\\news_links.json", start_urls)
