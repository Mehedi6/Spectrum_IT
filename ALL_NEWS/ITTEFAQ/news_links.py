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
    import html
    import urllib
    from urllib.parse import urljoin

    # Configure ChromeDriver
    chrome_options = Options()
    # Uncomment the next line to run in headless mode once debugging is complete
    # chrome_options.add_argument("--headless=new")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Necessary for some environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size to ensure all elements load
    chrome_options.add_argument("--disable-webgl")  # Disable WebGL to prevent related errors
    chrome_options.add_argument("--disable-software-rasterizer")  # Ensure software rendering
    chrome_options.add_argument("--use-gl=swiftshader")  # Force software GL rendering
    chrome_options.add_argument("--disable-extensions")  # Disable extensions for better performance
    chrome_options.add_argument("--disable-accelerated-2d-canvas")  # Disable 2D canvas acceleration
    chrome_options.add_argument("--disable-background-networking")  # Disable background networking
    chrome_options.add_argument("--disable-default-apps")  # Disable default apps
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    chrome_options.add_argument("--disable-plugins")  # Disable plugins
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("--mute-audio")  # Mute audio to avoid interruptions
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    chrome_options.add_argument("--silent")  # Suppress logs

    # Optional: Set a realistic user-agent to mimic a real browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/116.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)


    def get_news_type(url):
        # National News
        if 'national' in url:
            return ['national', 'general']
        elif 'country' in url:
            return ['national', 'all-country']
        elif 'capital' in url:
            return ['national', 'capital-city']
        elif 'law-and-court' in url:
            return ['national', 'law-justice']
        
        
        elif 'sports' in url:
            return ['sports', 'general']
        
        # International URLs
        elif 'world-news' in url:
            return ['international', 'general']

        # Economics URLs
        elif 'business' in url:
            return ['economics', 'general']
        
        # Politics URLs
        elif 'politics' in url:
            return ['politics', 'general']

        # Lifestyle URLs
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        
        
        # Entertainment URLs
        elif 'entertainment' in url:
            return ['entertainment', 'general']

        # Exile section
        elif 'probash' in url:
            return ['expatriate', 'general']        
        
        # Technology URLs
        elif 'tech' in url:
            return ['technology', 'general']

        # Campus URLs
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'education' in url:
            return ['education', 'general']
   

        # Job-Seeking URLs
        elif 'jobs' in url:
            return ['jobs', 'general']

        # Literature URLs
        elif 'literature' in url:
            return ['literature', 'general']
        
        # Interviews
        elif 'opinion' in url:
            return ['opinion', 'general']
        
        elif 'health' in url:
            return ['health', 'general']

        else:
            return ['others', 'general']
    
    # Scroll down the page a limited number of times
    def scroll_down():
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling

    # Click the "See More" button until it no longer appears
    def click_see_more_button():
        count = 0
        news_count = 15
        previous_article_count = 0
        while True:
            try:
                if count == 400:
                    break
                # Scroll down first to ensure the "See More" button is visible
                # scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 30)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@class="ajax_load_btn"]')
                ))

                try:
                    # Attempt to click the button
                    driver.execute_script("arguments[0].scrollIntoView();", see_more_button)
                    see_more_button.click()
                    count+=1
                    print(f"Clicked 'See More' button. {count} time(s)")
                    
                    time.sleep(3)  # Wait for more content to load
                    # Check if new content has been loaded
                    current_article_count = len(driver.find_elements(By.XPATH, '//a[@class="link_overlay"]'))  # Replace with appropriate selector for articles

                    if current_article_count == previous_article_count:
                        # Define the number of clicks
                        num_clicks = 10

                        for _ in range(num_clicks):
                            try:
                                see_more_button.click()
                                # Optional: wait for the page to load or for content to appear
                                time.sleep(3)  # You can adjust the wait time as needed (or use WebDriverWait)
                                current_article_count = len(driver.find_elements(By.XPATH, '//a[@class="link_overlay"]'))  # Replace with appropriate selector for articles
                                if current_article_count != previous_article_count:
                                    print("More new contents loaded.")
                                    count+=1
                                    break
                                
                            except Exception as e:
                                print(f"Error clicking the button: {e}")
                                break  # If there's an issue (like the button not being clickable), stop the loop
                        current_article_count = len(driver.find_elements(By.XPATH, '//a[@class="link_overlay"]'))  # Replace with appropriate selector for articles
                        if current_article_count == previous_article_count:
                            print("No new content loaded. Ending the loop.")
                            break
                    previous_article_count = current_article_count
                    news_count += 1
                except ElementClickInterceptedException:
                    # If click is intercepted, scroll a bit more and retry
                    print("Click intercepted, scrolling and retrying...")
                    scroll_down()
                    see_more_button.click()
                    count +=1

            except (TimeoutException, NoSuchElementException):
                # If no more "See More" button is found, break the loop
                print("No more 'See More' button found.")
                break

    # Extract links from loaded content
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        paths = ['//a[@class="link_overlay"]',
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
    try:
        with open(output_file_name, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []  # Initialize empty if file doesn't exist

    # Extract only new URLs not already in the file
    existing_urls = {item['url'] for item in existing_data}
    
    
    for url in urls_to_scrape:
        all_links = set()
        url = urllib.parse.unquote(url)
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        # Step 1: Scroll a limited number of times
        click_see_more_button()  # Limit to 10 scrolls
        news_type, news_subcategory = get_news_type(url)
        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        for link in links_data:
            if link not in {item[0] for item in all_links} and link not in existing_urls:  # Check if URL is not already in the set
                all_links.add((link, news_type, news_subcategory))
        
        
                
        # Step 3: Save the extracted unique links to a JSON file
        unique_links = [{"url": link[0], "news_type": link[1], "news_subcategory": link[2]} for link in all_links]  # Convert the set to a list of dicts
        
        filtered_new_data = [item for item in unique_links]

        # Append new data to existing data and write back to JSON
        existing_data.extend(filtered_new_data)
        with open(output_file_name, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        print(f"Saved {len(all_links)} new links to {output_file_name}")

    # Close the browser when done
    driver.quit()

# Example usage:
start_urls = [
                'https://www.ittefaq.com.bd/national',
                # 'https://www.ittefaq.com.bd/country',
                # 'https://www.ittefaq.com.bd/capital',

                # 'https://www.ittefaq.com.bd/politics',

            #     'https://www.ittefaq.com.bd/world-news',

            #     'https://www.ittefaq.com.bd/sports',

            #     'https://www.ittefaq.com.bd/entertainment',

            #     'https://www.ittefaq.com.bd/business',

            #     'https://www.ittefaq.com.bd/lifestyle',

            #     'https://www.ittefaq.com.bd/tech',

            #     'https://www.ittefaq.com.bd/opinion',

            #     'https://www.ittefaq.com.bd/health',
                
            #     'https://www.ittefaq.com.bd/law-and-court',

            #     'https://www.ittefaq.com.bd/education',
            #     'https://www.ittefaq.com.bd/campus',

            #     'https://www.ittefaq.com.bd/jobs',

            #     'https://www.ittefaq.com.bd/probash',

            #     'https://www.ittefaq.com.bd/literature', 

            #    'https://www.ittefaq.com.bd/news',


]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ALL_NEWS\\ITTEFAQ\\news_links.json", start_urls)
