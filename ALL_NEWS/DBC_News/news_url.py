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
    import urllib.parse

    # Configure ChromeDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)


    def get_news_type(url):
        # National News
        if 'national' in url:
            return ['national', 'all-bangladesh']
        elif 'district-news' in url:
            return ['national', 'district-news']
        elif 'রাজধানী' in url:  # "রাজধানী" in Bangla
            return ['national', 'capital']
        elif 'মহানগরী' in url:  # "মহানগরী" in Bangla
            return ['national', 'metropolitan']

        # Politics
        elif 'politics' in url:
            return ['politics', 'general']

        # Economy
        elif 'economy' in url:
            return ['economics', 'general']

        # Crime
        elif 'crime' in url:
            return ['crime', 'general']

        # International News
        elif 'ইটালী' in url:  # "ইটালী" in Bangla
            return ['international', 'italy']
        elif 'america' in url:
            return ['international', 'america']
        elif 'india' in url:
            return ['international', 'india']
        elif 'pakistan' in url:
            return ['international', 'pakistan']
        elif 'asia' in url:
            return ['international', 'asia']
        elif 'europe' in url:
            return ['international', 'europe']
        elif 'arab' in url:
            return ['international', 'arab']
        elif 'others-international' in url:
            return ['international', 'others']

        # Sports
        elif 'বিপিএল' in url:  # "বিপিএল" in Bangla
            return ['sports', 'bpl']
        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'others-sports' in url:
            return ['sports', 'others']

        # Entertainment
        elif 'dhallywood' in url:
            return ['entertainment', 'dhallywood']
        elif 'hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'television' in url:
            return ['entertainment', 'television']
        elif 'culture' in url:
            return ['entertainment', 'culture']
        elif 'others-entertainment' in url:
            return ['entertainment', 'others']

        # Opinion
        elif 'opinion' in url:
            return ['opinion', 'general']

        # Literature
        elif 'poem-literature' in url:
            return ['literature', 'poem']
        elif 'story-literature' in url:
            return ['literature', 'story']
        elif 'travel-literature' in url:
            return ['literature', 'travel']
        elif 'books-literature' in url:
            return ['literature', 'books']
        elif 'translation-literature' in url:
            return ['literature', 'translation']
        elif 'others-literature' in url:
            return ['literature', 'others']

        # Jobs
        elif 'job' in url:
            return ['jobs', 'general']
        elif 'career' in url:
            return ['jobs', 'career']
        elif 'announcement-job' in url:
            return ['jobs', 'announcement']
        elif 'counsel-job' in url:
            return ['jobs', 'counsel']


        # Lifestyle
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']

        # Science, Technology, and Education
        elif 'science-tech' in url:
            return ['technology', 'science-tech']
        elif 'education' in url:
            return ['education', 'general']

        # Health
        elif 'health' in url:
            return ['health', 'general']


        elif 'emigration' in url:
            return ['expatriate', 'general']
        
        elif 'travel' in url or 'where-to-travel' in url:
            return ['travel', 'general']
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
        
        paths = ['/html/body/div[1]/main/div[2]/div/div/div[1]/div[2]/div/div[1]/div/a',
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

        return links  # Return unique links

    # Collect all unique links across all pages
    all_links = set()
    for url in urls_to_scrape:
        
        url = urllib.parse.unquote(url)
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
    'https://dbcnews.tv/national',
    'https://dbcnews.tv/district-news',
    'https://dbcnews.tv/%E0%A6%B0%E0%A6%BE%E0%A6%9C%E0%A6%A7%E0%A6%BE%E0%A6%A8%E0%A7%80',
    'https://dbcnews.tv/%E0%A6%AE%E0%A6%B9%E0%A6%BE%E0%A6%A8%E0%A6%97%E0%A6%B0%E0%A7%80',

    'https://dbcnews.tv/politics',

    'https://dbcnews.tv/economy',

    'https://dbcnews.tv/crime',

    'https://dbcnews.tv/%E0%A6%87%E0%A6%9F%E0%A6%BE%E0%A6%B2%E0%A7%80',
    'https://dbcnews.tv/america',
    'https://dbcnews.tv/india',
    'https://dbcnews.tv/pakistan',
    'https://dbcnews.tv/asia',
    'https://dbcnews.tv/europe',
    'https://dbcnews.tv/arab',
    'https://dbcnews.tv/others-international',

    'https://dbcnews.tv/%E0%A6%AC%E0%A6%BF%E0%A6%AA%E0%A6%BF%E0%A6%8F%E0%A6%B2',
    'https://dbcnews.tv/cricket',
    'https://dbcnews.tv/football',
    'https://dbcnews.tv/others-sports',
    
    'https://dbcnews.tv/dhallywood',
    'https://dbcnews.tv/hollywood',
    'https://dbcnews.tv/bollywood',
    'https://dbcnews.tv/television',
    'https://dbcnews.tv/culture',
    'https://dbcnews.tv/others-entertainment',

    'https://dbcnews.tv/opinion',

    'https://dbcnews.tv/poem-literature',
    'https://dbcnews.tv/story-literature',
    'https://dbcnews.tv/travel-literature',
    'https://dbcnews.tv/books-literature',
    'https://dbcnews.tv/translation-literature',
    'https://dbcnews.tv/others-literature',

    #jobs
    'https://dbcnews.tv/job',
    'https://dbcnews.tv/career',
    'https://dbcnews.tv/announcement-job',
    'https://dbcnews.tv/counsel-job',

    'https://dbcnews.tv/lifestyle',

    'https://dbcnews.tv/science-tech',
    'https://dbcnews.tv/education',
    'https://dbcnews.tv/health',
    'https://dbcnews.tv/emigration',
    'https://dbcnews.tv/travel',
    'https://dbcnews.tv/where-to-travel',


]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DBC_News\\news_links.json", start_urls)
