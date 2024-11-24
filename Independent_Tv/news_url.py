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
        if 'country' in url:
            return ['national', 'all-bangladesh']
        elif 'national' in url:
            return ['national', 'general']
        elif 'national/dhaka' in url:
            return ['national', 'capital-city']

        # Politics
        elif 'politics' in url:
            return ['politics', 'general']

        # Economy
        elif 'economy' in url:
            if 'corporate' in url:
                return ['economy', 'corporate']
            elif 'share-market' in url:
                return ['economy', 'share-market']
            else:
                return ['economy', 'economy']

        # International News
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
        elif 'africa' in url:
            return ['international', 'africa']
        elif 'china' in url:
            return ['international', 'china']
        elif 'middle-east' in url:
            return ['international', 'middle-east']

        # Sports
        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'tennis' in url:
            return ['sports', 'tennis']
        elif 'other-sports' in url:
            return ['sports', 'others']

        # Entertainment
        elif 'dhallywood' in url:
            return ['entertainment', 'dhallywood']
        elif 'hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'television-stage' in url:
            return ['entertainment', 'television-stage']
        elif 'ott' in url:
            return ['entertainment', 'ott']
        elif 'tollywood' in url:
            return ['entertainment', 'tollywood']
        elif 'music' in url:
            return ['entertainment', 'music']
        elif 'dakshini-and-others' in url:
            return ['entertainment', 'dakshini-and-others']

        # Lifestyle
        elif 'lifestyle' in url:
            if 'interior' in url:
                return ['lifestyle', 'interior']
            elif 'fashion' in url:
                return ['lifestyle', 'fashion']
            elif 'beauty' in url:
                return ['lifestyle', 'beauty']
            elif 'food' in url:
                return ['lifestyle', 'food']
            elif 'relation' in url:
                return ['lifestyle', 'relation']
            else:
                return ['lifestyle', 'general']
        
        # Science and Technology
        elif 'science-tech' in url:
            if 'research' in url:
                return ['technology', 'research']
            elif 'gadget' in url:
                return ['technology', 'gadget']
            elif 'science' in url:
                return ['technology', 'science']
            elif 'social-media' in url:
                return ['technology', 'social-media']
            else:
                return ['technology', 'science-tech']
        
        
        elif 'travel' in url:
            return ['travel', 'general']
        # Health
        elif 'health' in url:
            return ['health', 'general']
        
        # Jobs
        elif 'jobs' in url:
            return ['jobs', 'general']
        
        # Education
        elif 'education' in url:
            return ['education', 'general']
        
        # Opinion
        elif 'opinion' in url:
            return ['opinion', 'general']
        
        # Probash (Expatriates)
        elif 'probash' in url:
            return ['expatriate', 'general']
        
        # Unknown category
        
        else:
            return ['others', 'general']
    
    # Scroll down the page a limited number of times
    def scroll_down():
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling

    def click_see_more_button():
        count = 0
        while True:
            try:
                # Scroll down first to ensure the "See More" button is visible
                scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@class="ajax_load_btn"]')
                ))

                try:
                    if count >=5:
                        break
                    # Attempt to click the button
                    see_more_button.click()
                    print("Clicked 'See More' button.")
                    count += 1
                    time.sleep(2)   # Wait for more content to load
                    # links_data = extract_links()
                    # return links_data
                      
                except ElementClickInterceptedException:
                    # If click is intercepted, scroll a bit more and retry
                    print("Click intercepted, scrolling and retrying...")
                    scroll_down()
                    see_more_button.click()

            except (TimeoutException, NoSuchElementException):
                # If no more "See More" button is found, break the loop
                print("No more 'See More' button found.")
                break

    # Extract links from loaded content
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        paths = ['/html/body/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div[1]/div/h2/a',
                 '/html/body/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/h2/a',
                 '/html/body/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/h2/a',
                 '/html/body/div[3]/div/div[2]/div/div/div[3]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div/h2/a', 
                 '/html/body/div[3]/div/div[2]/div/div/div[4]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div/h2/a',
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
    
    for url in urls_to_scrape:
        all_links = set()
        url = urllib.parse.unquote(url)
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

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

        print(f"Saved {len(filtered_new_data)} new links to {output_file_name}")

    # Close the browser when done
    driver.quit()

# Example usage:
start_urls = [
    'https://www.itvbd.com/national',
    'https://www.itvbd.com/country',
    'https://www.itvbd.com/country/dhaka'

    'https://www.itvbd.com/politics',
    
    'https://www.itvbd.com/world/africa',
    'https://www.itvbd.com/world/america',
    'https://www.itvbd.com/world/europe',
    'https://www.itvbd.com/world/asia',
    'https://www.itvbd.com/world/china',
    'https://www.itvbd.com/world/pakistan',
    'https://www.itvbd.com/world/india',
    'https://www.itvbd.com/world/middle-east',

    'https://www.itvbd.com/sports/cricket',
    'https://www.itvbd.com/sports/football',
    'https://www.itvbd.com/sports/tennis',
    'https://www.itvbd.com/sports/other-sports',

    'https://www.itvbd.com/entertainment/ott',
    'https://www.itvbd.com/entertainment/television-stage',
    'https://www.itvbd.com/entertainment/music',
    'https://www.itvbd.com/entertainment/dhallywood',
    'https://www.itvbd.com/entertainment/bollywood',
    'https://www.itvbd.com/entertainment/hollywood',
    'https://www.itvbd.com/entertainment/tollywood',
    'https://www.itvbd.com/entertainment/dakshini-and-others',
    
    'https://www.itvbd.com/lifestyle/interior',
    'https://www.itvbd.com/lifestyle/fashion',
    'https://www.itvbd.com/lifestyle/beauty',
    'https://www.itvbd.com/lifestyle/food',
    'https://www.itvbd.com/lifestyle/relation',

    'https://www.itvbd.com/lifestyle/travel',

    'https://www.itvbd.com/science-tech/research',
    'https://www.itvbd.com/science-tech/gadget',
    'https://www.itvbd.com/science-tech/science',
    'https://www.itvbd.com/science-tech/social-media',
    'https://www.itvbd.com/science-tech',

    'https://www.itvbd.com/economy/corporate',
    'https://www.itvbd.com/economy/share-market',
    'https://www.itvbd.com/economy',

    'https://www.itvbd.com/health',
    
    'https://www.itvbd.com/jobs',

    'https://www.itvbd.com/education',
    
    'https://www.itvbd.com/opinion',

    'https://www.itvbd.com/probash',





]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Independent_Tv\\news_links.json", start_urls)
