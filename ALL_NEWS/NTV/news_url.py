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
        if 'national' in url:
            return ['national', 'all-bangladesh']
        elif 'country' in url:
            if 'dhaka' in url:
                return ['national', 'dhaka']
            elif 'chitagong' in url:
                return ['national', 'chitagong']
            elif 'rajshahi' in url:
                return ['national', 'rajshahi']
            elif 'khulna' in url:
                return ['national', 'khulna']
            elif 'barishal' in url:
                return ['national', 'barishal']
            elif 'sylhet' in url:
                return ['national', 'sylhet']
            elif 'rangpur' in url:
                return ['national', 'rangpur']
            elif 'mymensing' in url:
                return ['national', 'mymensing']
            else:
                return ['national', 'other-region']
        
        if 'জাতীয়-সংসদ' in url:
            return ['politics', 'parliament']
        elif 'নির্বাচন-কমিশন' in url:
            return ['politics', 'election-commission']
        elif 'politics/awami-league' in url:
            return ['politics', 'awami-league']
        elif 'politics/bnp' in url:
            return ['politics', 'bnp']
        elif 'politics/jatiyo-party' in url:
            return ['politics', 'jatiyo-party']
        elif 'politics/jamat-e-islam' in url:
            return ['politics', 'jamat-e-islam']
        elif 'politics/other-politics' in url:
            return ['politics', 'other']
        
        # International
        elif 'foreign/asia' in url:
            return ['international', 'asia']
        elif 'foreign/middle-east' in url:
            return ['international', 'middle-east']
        elif 'foreign/europe' in url:
            return ['international', 'europe']
        elif 'foreign/america' in url:
            return ['international', 'america']
        elif 'foreign/africa' in url:
            return ['international', 'africa']
        elif 'অস্ট্রেলিয়া' in url:
            return ['international', 'australia']
        elif 'রাশিয়া-ইউক্রেন-যুদ্ধ' in url:
            return ['international', 'russia-ukraine']
        elif 'ইসরাইল-ফিলিস্তিন-যুদ্ধ' in url:
            return ['international', 'israel-palestine']

        # Economics
        elif 'business/stock-exchange' in url:
            return ['economics', 'stock-exchange']
        elif 'বাজেট' in url:
            return ['economics', 'budget']
        elif 'business/foreign-economy' in url:
            return ['economics', 'foreign-economy']
        elif 'business/power-and-fuel' in url:
            return ['economics', 'power-and-fuel']
        elif 'business/industry-and-trade' in url:
            return ['economics', 'industry-and-trade']
        elif 'business/money-and-investment' in url:
            return ['economics', 'money-and-investment']
        elif 'business/news' in url:
            return ['economics', 'news']
        elif 'গ্যাসের-দাম' in url:
            return ['economics', 'gas-price']
        elif 'সোনার-দাম' in url:
            return ['economics', 'gold-price']
        elif 'বাংলাদেশ-অর্থনীতি' in url:
            return ['economics', 'bangladesh-economy']
        
        #entertainment
        elif 'entertainment/dhallywood' in url:
            return ['entertainment', 'dhallywood']
        elif 'entertainment/bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'entertainment/hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'entertainment/television' in url:
            return ['entertainment', 'television']
        elif 'entertainment/songs' in url:
            return ['entertainment', 'songs']
        elif 'entertainment/stage' in url:
            return ['entertainment', 'stage']
        elif 'entertainment/face-to-face' in url:
            return ['entertainment', 'face-to-face']
        elif 'entertainment/radio' in url:
            return ['entertainment', 'radio']
        
        # Sports
        elif 'topic/টিভিতে-আজকের-খেলা' in url:
            return ['sports', 'todays-match']
        elif 'topic/বাংলাদেশ-ক্রিকেট' in url:
            return ['sports', 'bangladesh-cricket']
        elif 'topic/টি-২০-বিশ্বকাপ' in url:
            return ['sports', 't20-world-cup']
        elif 'topic/আইপিএল' in url:
            return ['sports', 'ipl']
        elif 'topic/বিপিএল' in url:
            return ['sports', 'bpl']
        elif 'sport/cricket' in url:
            return ['sports', 'cricket']
        elif 'sport/football' in url:
            return ['sports', 'football']
        elif 'topic/কোপা-আমেরিকা' in url:
            return ['sports', 'copa-america']
        elif 'topic/ইউরো' in url:
            return ['sports', 'euro']
        elif 'sport/hockey' in url:
            return ['sports', 'hockey']
        elif 'sport/tennis' in url:
            return ['sports', 'tennis']
        elif 'sport/other-sports' in url:
            return ['sports', 'other']

        # Technology
        elif 'tech-and-gadget/tech-news' in url:
            return ['technology', 'tech-news']
        elif 'tech-and-gadget/techsclusive' in url:
            return ['technology', 'techsclusive']
        elif 'tech-and-gadget/tech-talk' in url:
            return ['technology', 'tech-talk']
        elif 'tech-and-gadget/games' in url:
            return ['technology', 'games']
        elif 'tech-and-gadget/tricks' in url:
            return ['technology', 'tricks']
        elif 'tech-and-gadget/new-in-market' in url:
            return ['technology', 'new-in-market']

        # Education
        elif 'educations' in url:
            return ['education', 'general']
        elif 'topic/শিক্ষা-মন্ত্রণালয়' in url:
            return ['education', 'education-ministry']
        elif 'topic/নন-এমপিও' in url:
            return ['education', 'non-mpo']
        elif 'topic/এনটিআরসিএ' in url:
            return ['education', 'ntrca']
        elif 'topic/জাতীয়-বিশ্ববিদ্যালয়' in url:
            return ['education', 'national-university']
        elif 'topic/প্রতিবন্ধী-স্কুল' in url:
            return ['education', 'disabled-school']

        # Health
        elif 'health' in url:
            return ['health', 'general']
        elif 'health/corona' in url:
            return ['health', 'corona']
        elif 'topic/মানসিক-স্বাস্থ্য' in url:
            return ['health', 'mental-health']
        elif 'topic/নাগরিক-শৌচাগার-চিত্র' in url:
            return ['health', 'public-sanitation']

        # Lifestyle
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        elif 'lifestyle/tips' in url:
            return ['lifestyle', 'tips']
        elif 'lifestyle/news-corner' in url:
            return ['lifestyle', 'news-corner']
        elif 'lifestyle/food-blog' in url:
            return ['lifestyle', 'food-blog']
        elif 'lifestyle/fashion' in url:
            return ['lifestyle', 'fashion']
        elif 'lifestyle/special-feature' in url:
            return ['lifestyle', 'special-feature']
        elif 'lifestyle/foreign-fashion' in url:
            return ['lifestyle', 'foreign-fashion']
        elif 'lifestyle/foodies' in url:
            return ['lifestyle', 'foodies']
        elif 'lifestyle/beauty' in url:
            return ['lifestyle', 'beauty']
        elif 'topic/চুলের-যত্ন' in url:
            return ['lifestyle', 'hair-care']

        # Literature
        elif 'literature' in url:
            return ['literature', 'general']
        elif 'literature/poetry' in url:
            return ['literature', 'poetry']
        elif 'literature/short-stories' in url:
            return ['literature', 'short-stories']
        elif 'literature/articles' in url:
            return ['literature', 'articles']
        elif 'literature/interviews' in url:
            return ['literature', 'interviews']

        # Jobs
        elif 'jobs' in url:
            return ['jobs', 'general']

        # Crime
        elif 'law-and-crime' in url:
            return ['crime', 'general']

        # Travel
        elif 'journey' in url:
            return ['travel', 'general']
        elif 'journey/travel-tour' in url:
            return ['travel', 'travel-tour']
        elif 'journey/aviation' in url:
            return ['travel', 'aviation']
        elif 'journey/wonder' in url:
            return ['travel', 'wonder']
        elif 'tourism-news' in url or 'boundule' in url:
            return ['travel', 'tourism-news']
        
      
        else:
            return ['others', 'others']
    
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
                    (By.XPATH, '/html/body/div[3]/div/div[2]/main/div/div[2]/div/div[3]/div/div/div/div[2]/ul/li/a')
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
        
        # Find card elements containing news links
        paths = ['/html/body/div[3]/div/div[2]/main/div/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/a',
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
    'https://www.ntvbd.com/bangladesh/government',
    'https://www.ntvbd.com/bangladesh/law-and-rules',
    'https://www.ntvbd.com/bangladesh/accident',
    'https://www.ntvbd.com/bangladesh/obituary',
    'https://www.ntvbd.com/bangladesh/lost',

    #international
    'https://www.ntvbd.com/world/united-states',
    'https://www.ntvbd.com/world/united-kingdom',
    'https://www.ntvbd.com/world/canada',
    'https://www.ntvbd.com/world/india',
    'https://www.ntvbd.com/world/pakistan',
    'https://www.ntvbd.com/world/arab-world',
    'https://www.ntvbd.com/world/asia',
    'https://www.ntvbd.com/world/europe',
    'https://www.ntvbd.com/world/latin-america',
    'https://www.ntvbd.com/world/africa',
    'https://www.ntvbd.com/world/australia',
    'https://www.ntvbd.com/world/others',

    #sports
    'https://www.ntvbd.com/sports/cricket',
    'https://www.ntvbd.com/sports/football',
    'https://www.ntvbd.com/sports/tennis',
    'https://www.ntvbd.com/sports/athletics',
    'https://www.ntvbd.com/sports/hockey',
    'https://www.ntvbd.com/sports/others',

    #entertainment
    'https://www.ntvbd.com/entertainment/dhallywood',
    'https://www.ntvbd.com/entertainment/bollywood-and-others-',
    'https://www.ntvbd.com/entertainment/hollywood-and-others',
    'https://www.ntvbd.com/entertainment/tallywood',
    'https://www.ntvbd.com/entertainment/face-to-face',
    'https://www.ntvbd.com/entertainment/tv',
    'https://www.ntvbd.com/entertainment/music',
    'https://www.ntvbd.com/entertainment/dance',
    'https://www.ntvbd.com/entertainment/theatre',
    'https://www.ntvbd.com/entertainment/web-series-film',
    'https://www.ntvbd.com/entertainment/culture',
    ''
    
    'https://www.ntvbd.com/bangladesh/crime',

    'https://www.ntvbd.com/bangladesh/politics',

    
]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\NTV\\news_links.json", start_urls)
