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
        if 'c2dwq2nd40xt' in url:
            return ['national', 'all-bangladesh']
        elif 'cqywj91rkg6t' in url:
            return ['politics', 'general']
        elif 'c907347rezkt' in url:
            return ['international', 'general']
        elif 'cdr56gv542vt' in url:
            return ['international', 'india']
        elif 'cjgn7233zk5t' in url:
            return ['economics', 'general']
        elif 'cg7265yyxn1t' in url:
            return ['health', 'general']
        elif 'cdr56g57y01t' in url:
            return ['sports', 'general']
        elif 'c8y94k95v52t' in url:
            return ['technology', 'innovation-technology']
        

        else:
            return ['others', 'others']
    
    # Scroll down the page a limited number of times
    def scroll_down():
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling
    def click_see_more_button():
        while True:
            try:
                # Scroll down first to ensure the "See More" button is visible
                scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//span[@class="bbc-1u3fgrg"]//a[@aria-labelledby="pagination-next-page"]')
                ))

                try:
                    # Attempt to click the button
                    see_more_button.click()
                    print("Clicked 'See More' button.")
                    time.sleep(2)   # Wait for more content to load
                    links_data = extract_links()
                    return links_data
                      
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
        
        # Find card elements containing news links
        paths = ['//h2[@class="bbc-qqcsu8 e47bds20"]/a',
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
        count = 0
        all_links = set()
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        news_type, news_subcategory = get_news_type(url)
        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        for link in links_data:
            if link not in {item[0] for item in all_links}:  # Check if URL is not already in the set
                all_links.add((link, news_type, news_subcategory))
        
        
        while count <5:
            links_data = click_see_more_button()
            count += 1
            try:
                for link in links_data:
                    if link not in {item[0] for item in all_links}:  # Check if URL is not already in the set
                        all_links.add((link, news_type, news_subcategory))
            except Exception as e:
                print(f"Error {e}")
        
    
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
    'https://www.bbc.com/bengali/topics/c2dwq2nd40xt',  #national
    'https://www.bbc.com/bengali/topics/cqywj91rkg6t',   #politics
    'https://www.bbc.com/bengali/topics/c907347rezkt',   #international
    'https://www.bbc.com/bengali/topics/cdr56gv542vt',  #india 
    'https://www.bbc.com/bengali/topics/cjgn7233zk5t',  #ecocnomics
    'https://www.bbc.com/bengali/topics/cg7265yyxn1t',  #health
    'https://www.bbc.com/bengali/topics/cdr56g57y01t',  #sports
    'https://www.bbc.com/bengali/topics/c8y94k95v52t',  #technology

]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\BBC_News_Bangla\\news_links.json", start_urls)
