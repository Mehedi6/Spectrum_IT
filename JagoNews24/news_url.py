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
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)


    def get_news_type(url):
        if 'national' in url:
            return ['national', 'general']
        elif 'country' in url:
            return ['national', 'all-bangladesh']
        elif 'agriculture-and-nature' in url:
            return ['national', 'agriculture-and-nature']
        elif 'law-courts' in url:
            return ['national', 'law-courts']
        
        elif 'politics' in url:
            return ['politics', 'general']
        
        elif 'ব্যবসা-বাণিজ্য' in url:
            return ['economics', 'business']
        elif 'বিনিয়োগ' in url:
            return ['economics', 'investment']
        elif 'শেয়ার-বাজার' in url:
            return ['economics', 'stock-market']
        elif 'বাংলাদেশ-ব্যাংক' in url:
            return ['economics', 'bangladesh-bank']
        elif 'বিশ্বব্যাংক' in url:
            return ['economics', 'world-bank']
        elif 'উন্নয়ন-প্রকল্প' in url:
            return ['economics', 'development-project']
        
        elif 'ইসরায়েল-ফিলিস্তিন-সংঘাত' in url:
            return ['international', 'israel-palestine war']
        elif 'রাশিয়া-ইউক্রেন-যুদ্ধ' in url:
            return ['international', 'russia-ukraine war']
        elif 'ভারত' in url:
            return ['international', 'india']
        elif 'পাকিস্তান' in url:
            return ['international', 'pakistan']
        elif 'চীন' in url:
            return ['international', 'china']
        elif 'যুক্তরাষ্ট্র' in url:
            return ['international', 'usa']
        elif 'মালয়েশিয়া' in url:
            return ['international', 'malaysia']
        elif 'সৌদি-আরব' in url:
            return ['international', 'saudi arabia']
        elif 'ইরান' in url:
            return ['international', 'iran']
        elif 'ইউরোপ' in url:
            return ['international', 'europe']
        

        


        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'বিপিএল' in url:
            return ['sports', 'bpl']
        elif 'আইপিএল' in url:
            return ['sports', 'ipl']
        
        elif 'সরকারি-চাকরি' in url:
            return ['jobs', 'govt-job']
        elif 'বেসরকারি-চাকরি' in url:
            return ['jobs', 'private-job']
        elif 'ব্যাংকে-চাকরি' in url:
            return ['jobs', 'bank-job']
        elif 'শিক্ষক-নিয়োগ' in url:
            return ['jobs', 'teachers-recruitment']
        elif 'বিসিএস' in url:
            return ['jobs', 'bcs']
        elif 'বিপিএসসি' in url:
            return ['jobs', 'bpsc']
        elif 'এনজিও' in url:
            return ['jobs', 'ngo']
        elif 'ক্যারিয়ার' in url:
            return ['jobs', 'career']
        
        elif 'নাটক' in url:
            return ['entertainment', 'drama']
        elif 'বাংলা-মুভি' in url:
            return ['entertainment', 'bangla-cinema']
        elif 'ভারতীয়-সিনেমা' in url:
            return ['entertainment', 'indian-films']
        elif 'বিশ্বচলচ্চিত্র' in url:
            return ['entertainment', 'world-films']
        elif 'টেলিভিশন-অনুষ্ঠান' in url:
            return ['entertainment', 'television-programme']
        elif 'ওটিটি' in url:
            return ['entertainment', 'ott']
        elif 'গান' in url:
            return ['entertainment', 'song']
        elif 'তারকাকথন' in url:
            return ['entertainment', 'interview']
        elif 'hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'bollywood' in url:
            return ['entertainment', 'bollywood']
        
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        
        elif 'technology' in url:
            return ['technology', 'general']
        
        elif 'travel' in url:
            return ['travel', 'general']
        
        elif 'health' in url:
            return ['health', 'general']

        elif 'education' in url:
            return ['education', 'general']
        elif 'campus' in url:
            return ['education', 'campus']
        
        elif 'probash' in url:
            return ['expatriate', 'general']
        elif 'literature' in url:
            return ['literature', 'general']
        elif 'opinion' in url:
            return ['opinion', 'general']
        
        else:
            return ['others', 'general']
    
    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling
    
    # Click the "See More" button until it no longer appears
    
    def click_see_more_button():
        count = 0
        while True:
            try:
                # Scroll down first to ensure the "See More" button is visible
                scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//div[@class="text-center paddingBottom20"]')
                ))

                try:
                    if count == 5:
                        break
                    # Attempt to click the button
                    see_more_button.click()
                    print("Clicked 'See More' button.")
                    count +=1
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

    # Extract links from loaded content
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        # Find card elements containing news links
        paths = ['/html/body/section[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/h3/a',
                '/html/body/main/section/div/div[2]/div[2]/div[1]/div/div/div/div[2]/div/h3/a',
                '/html/body/main/section/div/div[2]/div[2]/div[3]/div[7]/div/div/div[1]/div/a'
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
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        # Step 1: Scroll a limited number of times
        click_see_more_button()
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
    'https://www.jagonews24.com/national',
    'https://www.jagonews24.com/country',
    'https://www.jagonews24.com/agriculture-and-nature',
    'https://www.jagonews24.com/law-courts',

    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A7%8D%E0%A6%AF%E0%A6%AC%E0%A6%B8%E0%A6%BE-%E0%A6%AC%E0%A6%BE%E0%A6%A3%E0%A6%BF%E0%A6%9C%E0%A7%8D%E0%A6%AF',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%A8%E0%A6%BF%E0%A7%9F%E0%A7%8B%E0%A6%97',
    'https://www.jagonews24.com/topic/%E0%A6%B6%E0%A7%87%E0%A7%9F%E0%A6%BE%E0%A6%B0-%E0%A6%AC%E0%A6%BE%E0%A6%9C%E0%A6%BE%E0%A6%B0',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6-%E0%A6%AC%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%82%E0%A6%95',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%8D%E0%A6%AC%E0%A6%AC%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%82%E0%A6%95',
    'https://www.jagonews24.com/topic/%E0%A6%89%E0%A6%A8%E0%A7%8D%E0%A6%A8%E0%A7%9F%E0%A6%A8-%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%95%E0%A6%B2%E0%A7%8D%E0%A6%AA',

    'https://www.jagonews24.com/politics',

    'https://www.jagonews24.com/topic/%E0%A6%87%E0%A6%B8%E0%A6%B0%E0%A6%BE%E0%A7%9F%E0%A7%87%E0%A6%B2-%E0%A6%AB%E0%A6%BF%E0%A6%B2%E0%A6%BF%E0%A6%B8%E0%A7%8D%E0%A6%A4%E0%A6%BF%E0%A6%A8-%E0%A6%B8%E0%A6%82%E0%A6%98%E0%A6%BE%E0%A6%A4',
    'https://www.jagonews24.com/topic/%E0%A6%B0%E0%A6%BE%E0%A6%B6%E0%A6%BF%E0%A7%9F%E0%A6%BE-%E0%A6%87%E0%A6%89%E0%A6%95%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A8-%E0%A6%AF%E0%A7%81%E0%A6%A6%E0%A7%8D%E0%A6%A7',
    'https://www.jagonews24.com/topic/%E0%A6%AD%E0%A6%BE%E0%A6%B0%E0%A6%A4',
    'https://www.jagonews24.com/topic/%E0%A6%AA%E0%A6%BE%E0%A6%95%E0%A6%BF%E0%A6%B8%E0%A7%8D%E0%A6%A4%E0%A6%BE%E0%A6%A8',
    'https://www.jagonews24.com/topic/%E0%A6%9A%E0%A7%80%E0%A6%A8',
    'https://www.jagonews24.com/topic/%E0%A6%AF%E0%A7%81%E0%A6%95%E0%A7%8D%E0%A6%A4%E0%A6%B0%E0%A6%BE%E0%A6%B7%E0%A7%8D%E0%A6%9F%E0%A7%8D%E0%A6%B0',
    'https://www.jagonews24.com/topic/%E0%A6%AE%E0%A6%BE%E0%A6%B2%E0%A7%9F%E0%A7%87%E0%A6%B6%E0%A6%BF%E0%A7%9F%E0%A6%BE',
    'https://www.jagonews24.com/topic/%E0%A6%B8%E0%A7%8C%E0%A6%A6%E0%A6%BF-%E0%A6%86%E0%A6%B0%E0%A6%AC',
    'https://www.jagonews24.com/topic/%E0%A6%87%E0%A6%B0%E0%A6%BE%E0%A6%A8',
    'https://www.jagonews24.com/topic/%E0%A6%87%E0%A6%89%E0%A6%B0%E0%A7%8B%E0%A6%AA',

    'https://www.jagonews24.com/sports/cricket',
    'https://www.jagonews24.com/sports/football',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%AA%E0%A6%BF%E0%A6%8F%E0%A6%B2',
    'https://www.jagonews24.com/topic/%E0%A6%86%E0%A6%87%E0%A6%AA%E0%A6%BF%E0%A6%8F%E0%A6%B2',
    
    'https://www.jagonews24.com/topic/%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0%E0%A6%BF-%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A7%87%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0%E0%A6%BF-%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%82%E0%A6%95%E0%A7%87-%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF',
    'https://www.jagonews24.com/topic/%E0%A6%B6%E0%A6%BF%E0%A6%95%E0%A7%8D%E0%A6%B7%E0%A6%95-%E0%A6%A8%E0%A6%BF%E0%A7%9F%E0%A7%8B%E0%A6%97',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%8F%E0%A6%B8',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%AA%E0%A6%BF%E0%A6%8F%E0%A6%B8%E0%A6%B8%E0%A6%BF',
    'https://www.jagonews24.com/topic/%E0%A6%8F%E0%A6%A8%E0%A6%9C%E0%A6%BF%E0%A6%93',
    'https://www.jagonews24.com/topic/%E0%A6%95%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%B0%E0%A6%BF%E0%A7%9F%E0%A6%BE%E0%A6%B0',
    
    'https://www.jagonews24.com/topic/%E0%A6%A8%E0%A6%BE%E0%A6%9F%E0%A6%95',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE-%E0%A6%AE%E0%A7%81%E0%A6%AD%E0%A6%BF',
    'https://www.jagonews24.com/topic/%E0%A6%AD%E0%A6%BE%E0%A6%B0%E0%A6%A4%E0%A7%80%E0%A7%9F-%E0%A6%B8%E0%A6%BF%E0%A6%A8%E0%A7%87%E0%A6%AE%E0%A6%BE',
    'https://www.jagonews24.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%8D%E0%A6%AC%E0%A6%9A%E0%A6%B2%E0%A6%9A%E0%A7%8D%E0%A6%9A%E0%A6%BF%E0%A6%A4%E0%A7%8D%E0%A6%B0',
    'https://www.jagonews24.com/topic/%E0%A6%9F%E0%A7%87%E0%A6%B2%E0%A6%BF%E0%A6%AD%E0%A6%BF%E0%A6%B6%E0%A6%A8-%E0%A6%85%E0%A6%A8%E0%A7%81%E0%A6%B7%E0%A7%8D%E0%A6%A0%E0%A6%BE%E0%A6%A8',
    'https://www.jagonews24.com/topic/%E0%A6%93%E0%A6%9F%E0%A6%BF%E0%A6%9F%E0%A6%BF',
    'https://www.jagonews24.com/topic/%E0%A6%97%E0%A6%BE%E0%A6%A8',
    'https://www.jagonews24.com/topic/%E0%A6%A4%E0%A6%BE%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%95%E0%A6%A5%E0%A6%A8',
    'https://www.jagonews24.com/entertainment/hollywood',
    'https://www.jagonews24.com/entertainment/bollywood',

    'https://www.jagonews24.com/lifestyle',

    'https://www.jagonews24.com/technology',
    
    'https://www.jagonews24.com/travel',

    'https://www.jagonews24.com/education',
    'https://www.jagonews24.com/campus',
    
    'https://www.jagonews24.com/health',

    'https://www.jagonews24.com/probash'

    'https://www.jagonews24.com/opinion',

    'https://www.jagonews24.com/literature',

]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\JagoNews24\\news_links.json", start_urls)
