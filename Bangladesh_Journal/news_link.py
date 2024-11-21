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
        if 'district-upazila' in url:
            return ['national', 'district-upazila']
        elif 'mofossol' in url:
            return ['national', 'rural']
        elif 'metropoliton' in url:
            return ['national', 'metropoliton-city']
        elif 'chittagong' in url:
            return ['national', 'chittagong']
        elif 'other/law-court' in url:
            return ['national', 'law-court']
        elif 'other/features' in url:
            return ['national', 'features']
        
        elif 'india' in url:
            return ['international', 'india']
        elif 'asia' in url:
            return ['international', 'asia']
        elif 'middle-east' in url:
            return ['international', 'middle-east']
        elif 'america' in url:
            return ['international', 'america']
        elif 'europe' in url:
            return ['international', 'europe']
        elif 'other' in url:
            return ['international', 'others']
        
        elif 'politics' in url:
            return ['politics', 'general']
        
        elif 'finance-business/banking-insurance' in url:
            return ['economics', 'banking-insurance']
        elif 'finance-business/share-bazar' in url:
            return ['economics', 'stock-market']
        elif 'economics/agriculture' in url:
            return ['economics', 'agriculture']
        elif 'economics/art' in url:
            return ['economics', 'industry']
        elif 'economics/business-trade' in url:
            return ['economics', 'business-trade']
        elif 'economics/electricity-and-fuel' in url:
            return ['economics', 'electricity-and-fuel']
        elif 'economics/telecom' in url:
            return ['economics', 'telecom']
        elif 'economics/world-economy' in url:
            return ['economics', 'world-economy']
        elif 'economics/corporate-world' in url:
            return ['economics', 'corporate-world']
        elif 'economics/other' in url:
            return ['economics', 'others']
       
        elif 'entertainment/drama' in url:
            return ['entertainment', 'drama']
        elif 'entertainment/movies' in url:
            return ['entertainment', 'movies']
        elif 'entertainment/song' in url:
            return ['entertainment', 'song']
        elif 'entertainment/drama' in url:
            return ['entertainment', 'drama']
        
        elif 'sports/cricket' in url:
            return ['sports', 'cricket']
        elif 'sports/football' in url:
            return ['sports', 'football']
        elif 'sports/other' in url:
            return ['sports', 'others']
        
        elif 'life-style/fashion' in url:
            return ['lifestyle', 'fashion']
        elif 'life-style/shapes' in url:
            return ['lifestyle', 'shapes']
        elif 'life-style/cooking' in url:
            return ['lifestyle', 'cooking']
        elif 'life-style/shopping' in url:
            return ['lifestyle', 'shopping']
        elif 'life-style/history-heritage' in url:
            return ['lifestyle', 'history-heritage']
        elif 'life-style/other' in url:
            return ['lifestyle', 'others']
        
        elif 'information-technology/mobile' in url:
            return ['technology', 'mobile']
        elif 'information-technology/tech' in url:
            return ['technology', 'tech']
        elif 'information-technology/computer' in url:
            return ['technology', 'computer']
        elif 'information-technology/apps' in url:
            return ['technology', 'apps']
        elif 'information-technology/innovation' in url:
            return ['technology', 'innovation']
        elif 'information-technology/other' in url:
            return ['technology', 'other']
        
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'travel' in url:
            return ['travel', 'general']
        elif 'health' in url:
            return ['health', 'general']
        elif 'health/coronavirus' in url:
            return ['health', 'coronavirus']
        elif 'other/opinion' in url:
            return ['opinion', 'general']
        
        elif 'other/job-market' in url:
            return ['jobs', 'general']
        
        elif 'other/offense' in url:
            return ['crime', 'general']
        
        elif 'other/emigration' in url:
            return ['expatriate', 'general']
        
        elif 'literature-and-culture' in url:
            return ['literature-and-culture', 'general']
        elif 'literature-and-culture/story' in url:
            return ['literature-and-culture', 'story']
        elif 'literature-and-culture/poem' in url:
            return ['literature-and-culture', 'poem']

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
                    (By.XPATH, '//li[@class="next-btn "]/a')
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
        card_elements = driver.find_elements(By.XPATH, '//div[@class="col-md-6"]/a')
        
        print(f"Found {len(card_elements)} card elements.")

        for card in card_elements:
            link = card.get_attribute('href')
            if link:
                links.add(link)
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
    'https://www.bd-journal.com/all-news/bangladesh/district-upazila',
    'https://www.bd-journal.com/all-news/bangladesh/mofossol',
    'https://www.bd-journal.com/all-news/bangladesh/metropoliton',
    'https://www.bd-journal.com/all-news/bangladesh/chittagong',
    'https://www.bd-journal.com/all-news/other/law-court',

    'https://www.bd-journal.com/all-news/international/india',
    'https://www.bd-journal.com/all-news/international/asia',
    'https://www.bd-journal.com/all-news/international/middle-east',
    'https://www.bd-journal.com/all-news/international/america',
    'https://www.bd-journal.com/all-news/international/europe',
    'https://www.bd-journal.com/all-news/international/other',
    'https://www.bd-journal.com/all-news/politics',
    'https://www.bd-journal.com/all-news/finance-business/banking-insurance',
    'https://www.bd-journal.com/all-news/finance-business/share-bazar',
    'https://www.bd-journal.com/all-news/economics/agriculture',
    'https://www.bd-journal.com/all-news/economics/art',
    'https://bd-journal.com/all-news/economics/business-trade',
    'https://www.bd-journal.com/all-news/economics/electricity-and-fuel',
    'https://www.bd-journal.com/all-news/economics/telecom',
    'https://www.bd-journal.com/all-news/economics/world-economy',
    'https://www.bd-journal.com/all-news/economics/corporate-world',
    'https://www.bd-journal.com/all-news/economics/other',
    'https://www.bd-journal.com/all-news/entertainment/drama',
    'https://www.bd-journal.com/all-news/entertainment/movies',
    'https://www.bd-journal.com/all-news/entertainment/song',
    'https://www.bd-journal.com/all-news/sports/cricket',
    'https://www.bd-journal.com/all-news/sports/football',
    'https://www.bd-journal.com/all-news/sports/other',
    'https://www.bd-journal.com/all-news/life-style/fashion',
    'https://www.bd-journal.com/all-news/life-style/shapes',
    'https://www.bd-journal.com/all-news/life-style/cooking',
    'https://www.bd-journal.com/all-news/life-style/shopping',
    'https://www.bd-journal.com/all-news/life-style/history-heritage',
    'https://www.bd-journal.com/all-news/life-style/other',

    'https://www.bd-journal.com/all-news/life-style/travel',

    'https://www.bd-journal.com/all-news/information-technology/mobile',
    'https://www.bd-journal.com/all-news/information-technology/tech',
    'https://www.bd-journal.com/all-news/information-technology/computer',
    'https://www.bd-journal.com/all-news/information-technology/apps',
    'https://www.bd-journal.com/all-news/information-technology/innovation',
    'https://www.bd-journal.com/all-news/information-technology/other',

    'https://www.bd-journal.com/all-news/education/campus',

    'https://www.bd-journal.com/all-news/other/health',

    'https://www.bd-journal.com/all-news/other/opinion',

    'https://www.bd-journal.com/all-news/other/features',

    'https://www.bd-journal.com/all-news/other/job-market',

    'https://www.bd-journal.com/all-news/other/offense',

    'https://www.bd-journal.com/all-news/other/emigration',

    'https://www.bd-journal.com/all-news/other/literature-and-culture',

    'https://www.bd-journal.com/all-news/literature-and-culture/story',

    'https://www.bd-journal.com/all-news/literature-and-culture/poem',

    'https://www.bd-journal.com/all-news/health/coronavirus',





]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Bangladesh_Journal\\news_links.json", start_urls)
