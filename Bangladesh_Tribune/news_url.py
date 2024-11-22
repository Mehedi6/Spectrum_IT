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
        
        # Find card elements containing news links
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
    #national
    'https://www.banglatribune.com/national',
    'https://www.banglatribune.com/country/dhaka',
    'https://www.banglatribune.com/country/chitagong',
    'https://www.banglatribune.com/country/rajshahi',
    'https://www.banglatribune.com/country/khulna',
    'https://www.banglatribune.com/country/barishal',
    'https://www.banglatribune.com/country/sylhet',
    'https://www.banglatribune.com/country/rangpur',
    'https://www.banglatribune.com/country/mymensing',

    #politics
    'https://www.banglatribune.com/topic/%E0%A6%9C%E0%A6%BE%E0%A6%A4%E0%A7%80%E0%A7%9F-%E0%A6%B8%E0%A6%82%E0%A6%B8%E0%A6%A6',
    'https://www.banglatribune.com/topic/%E0%A6%A8%E0%A6%BF%E0%A6%B0%E0%A7%8D%E0%A6%AC%E0%A6%BE%E0%A6%9A%E0%A6%A8-%E0%A6%95%E0%A6%AE%E0%A6%BF%E0%A6%B6%E0%A6%A8',
    'https://www.banglatribune.com/politics/awami-league',
    'https://www.banglatribune.com/politics/bnp',
    'https://www.banglatribune.com/politics/jatiyo-party',
    'https://www.banglatribune.com/politics/jamat-e-islam',
    'https://www.banglatribune.com/politics/other-politics',

    #international
    'https://www.banglatribune.com/foreign/asia',
    'https://www.banglatribune.com/foreign/middle-east',
    'https://www.banglatribune.com/foreign/europe',
    'https://www.banglatribune.com/foreign/america',
    'https://www.banglatribune.com/foreign/africa',
    'https://www.banglatribune.com/topic/%E0%A6%85%E0%A6%B8%E0%A7%8D%E0%A6%9F%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%B2%E0%A6%BF%E0%A7%9F%E0%A6%BE',
    'https://www.banglatribune.com/topic/%E0%A6%B0%E0%A6%BE%E0%A6%B6%E0%A6%BF%E0%A7%9F%E0%A6%BE-%E0%A6%87%E0%A6%89%E0%A6%95%E0%A7%8D%E0%A6%B0%E0%A7%87%E0%A6%A8-%E0%A6%AF%E0%A7%81%E0%A6%A6%E0%A7%8D%E0%A6%A7',
    'https://www.banglatribune.com/topic/%E0%A6%87%E0%A6%B8%E0%A6%B0%E0%A6%BE%E0%A6%87%E0%A6%B2-%E0%A6%AB%E0%A6%BF%E0%A6%B2%E0%A6%BF%E0%A6%B8%E0%A7%8D%E0%A6%A4%E0%A6%BF%E0%A6%A8-%E0%A6%AF%E0%A7%81%E0%A6%A6%E0%A7%8D%E0%A6%A7',

    #economics
    'https://www.banglatribune.com/business/stock-exchange',
    'https://www.banglatribune.com/topic/%E0%A6%AC%E0%A6%BE%E0%A6%9C%E0%A7%87%E0%A6%9F',
    'https://banglatribune.com/business/foreign-economy',
    'https://www.banglatribune.com/business/power-and-fuel',
    'https://www.banglatribune.com/business/industry-and-trade',
    'https://www.banglatribune.com/business/industry-and-trade',
    'https://www.banglatribune.com/business/money-and-investment',
    'https://www.banglatribune.com/business/news',
    'https://www.banglatribune.com/topic/%E0%A6%97%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%B8%E0%A7%87%E0%A6%B0-%E0%A6%A6%E0%A6%BE%E0%A6%AE',
    'https://www.banglatribune.com/topic/%E0%A6%B8%E0%A7%8B%E0%A6%A8%E0%A6%BE%E0%A6%B0-%E0%A6%A6%E0%A6%BE%E0%A6%AE',
    'https://banglatribune.com/topic/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6-%E0%A6%85%E0%A6%B0%E0%A7%8D%E0%A6%A5%E0%A6%A8%E0%A7%80%E0%A6%A4%E0%A6%BF',

    #entertainment
    'https://www.banglatribune.com/entertainment/dhallywood',
    'https://www.banglatribune.com/entertainment/bollywood',
    'https://www.banglatribune.com/entertainment/hollywood',
    'https://www.banglatribune.com/entertainment/television',
    'https://www.banglatribune.com/entertainment/songs',
    'https://www.banglatribune.com/entertainment/stage',
    'https://www.banglatribune.com/entertainment/face-to-face',
    'https://www.banglatribune.com/entertainment/radio',

    #sports
    'https://www.banglatribune.com/topic/%E0%A6%9F%E0%A6%BF%E0%A6%AD%E0%A6%BF%E0%A6%A4%E0%A7%87-%E0%A6%86%E0%A6%9C%E0%A6%95%E0%A7%87%E0%A6%B0-%E0%A6%96%E0%A7%87%E0%A6%B2%E0%A6%BE',
    'https://www.banglatribune.com/topic/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6-%E0%A6%95%E0%A7%8D%E0%A6%B0%E0%A6%BF%E0%A6%95%E0%A7%87%E0%A6%9F',
    'https://www.banglatribune.com/topic/%E0%A6%9F%E0%A6%BF-%E0%A7%A8%E0%A7%A6-%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%8D%E0%A6%AC%E0%A6%95%E0%A6%BE%E0%A6%AA',
    'https://www.banglatribune.com/topic/%E0%A6%86%E0%A6%87%E0%A6%AA%E0%A6%BF%E0%A6%8F%E0%A6%B2',
    'https://www.banglatribune.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%AA%E0%A6%BF%E0%A6%8F%E0%A6%B2'
    'https://www.banglatribune.com/sport/cricket',
    'https://www.banglatribune.com/sport/football',
    'https://www.banglatribune.com/topic/%E0%A6%95%E0%A7%8B%E0%A6%AA%E0%A6%BE-%E0%A6%86%E0%A6%AE%E0%A7%87%E0%A6%B0%E0%A6%BF%E0%A6%95%E0%A6%BE',
    'https://www.banglatribune.com/topic/%E0%A6%87%E0%A6%89%E0%A6%B0%E0%A7%8B',
    'https://www.banglatribune.com/sport/hockey',
    'https://www.banglatribune.com/sport/tennis',
    'https://www.banglatribune.com/sport/other-sports',
    
    #technology
    'https://www.banglatribune.com/tech-and-gadget/tech-news',
    'https://www.banglatribune.com/tech-and-gadget/techsclusive',
    'https://www.banglatribune.com/tech-and-gadget/tech-talk',
    'https://www.banglatribune.com/tech-and-gadget/games',
    'https://www.banglatribune.com/tech-and-gadget/tricks',
    'https://www.banglatribune.com/tech-and-gadget/new-in-market',

    #education
    'https://www.banglatribune.com/educations',
    'https://www.banglatribune.com/topic/%E0%A6%B6%E0%A6%BF%E0%A6%95%E0%A7%8D%E0%A6%B7%E0%A6%BE-%E0%A6%AE%E0%A6%A8%E0%A7%8D%E0%A6%A4%E0%A7%8D%E0%A6%B0%E0%A6%A3%E0%A6%BE%E0%A6%B2%E0%A7%9F',
    'https://www.banglatribune.com/topic/%E0%A6%A8%E0%A6%A8-%E0%A6%8F%E0%A6%AE%E0%A6%AA%E0%A6%BF%E0%A6%93',
    'https://www.banglatribune.com/topic/%E0%A6%8F%E0%A6%A8%E0%A6%9F%E0%A6%BF%E0%A6%86%E0%A6%B0%E0%A6%B8%E0%A6%BF%E0%A6%8F',
    'https://www.banglatribune.com/topic/%E0%A6%9C%E0%A6%BE%E0%A6%A4%E0%A7%80%E0%A7%9F-%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%8D%E0%A6%AC%E0%A6%AC%E0%A6%BF%E0%A6%A6%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%B2%E0%A7%9F',
    'https://www.banglatribune.com/topic/%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%A4%E0%A6%BF%E0%A6%AC%E0%A6%A8%E0%A7%8D%E0%A6%A7%E0%A7%80-%E0%A6%B8%E0%A7%8D%E0%A6%95%E0%A7%81%E0%A6%B2',

    #health
    'https://www.banglatribune.com/health',
    'https://www.banglatribune.com/health/corona',
    'https://www.banglatribune.com/topic/%E0%A6%AE%E0%A6%BE%E0%A6%A8%E0%A6%B8%E0%A6%BF%E0%A6%95-%E0%A6%B8%E0%A7%8D%E0%A6%AC%E0%A6%BE%E0%A6%B8%E0%A7%8D%E0%A6%A5%E0%A7%8D%E0%A6%AF',
    'https://www.banglatribune.com/topic/%E0%A6%A8%E0%A6%BE%E0%A6%97%E0%A6%B0%E0%A6%BF%E0%A6%95-%E0%A6%B6%E0%A7%8C%E0%A6%9A%E0%A6%BE%E0%A6%97%E0%A6%BE%E0%A6%B0-%E0%A6%9A%E0%A6%BF%E0%A6%A4%E0%A7%8D%E0%A6%B0?utm_source=healthcat&utm_medium=siteuser',

    #lifestyle
    'https://www.banglatribune.com/lifestyle/tips',
    'https://www.banglatribune.com/lifestyle/news-corner',
    'https://www.banglatribune.com/lifestyle/food-blog',
    'https://www.banglatribune.com/lifestyle/fashion',
    'https://www.banglatribune.com/lifestyle/special-feature',
    'https://www.banglatribune.com/lifestyle/foreign-fashion',
    'https://www.banglatribune.com/lifestyle/health-style',
    'https://www.banglatribune.com/lifestyle/foodies',
    'https://www.banglatribune.com/lifestyle/beauty',
    'https://www.banglatribune.com/topic/%E0%A6%9A%E0%A7%81%E0%A6%B2%E0%A7%87%E0%A6%B0-%E0%A6%AF%E0%A6%A4%E0%A7%8D%E0%A6%A8',
    'https://www.banglatribune.com/lifestyle/%E0%A6%85%E0%A6%A8%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%A8%E0%A7%8D%E0%A6%AF',

    #literature
    'https://www.banglatribune.com/literature/ceremony',
    'https://www.banglatribune.com/literature/poetry',
    'https://www.banglatribune.com/literature/junket',
    'https://www.banglatribune.com/literature/small-papers',
    'https://www.banglatribune.com/literature/short-stories',
    'https://www.banglatribune.com/literature/series',
    'https://www.banglatribune.com/literature/new-books',
    'https://www.banglatribune.com/literature/readers-comment',
    'https://www.banglatribune.com/literature/manuscript',
    'https://www.banglatribune.com/literature/prize',
    'https://www.banglatribune.com/literature/articles',
    'https://www.banglatribune.com/literature/speech',
    'https://www.banglatribune.com/literature/interviews',
    'https://www.banglatribune.com/literature/review-literature',
    
    #jobs
    'https://www.banglatribune.com/jobs',

    #crime
    'https://www.banglatribune.com/law-and-crime',

    #travel
    'https://www.banglatribune.com/lifestyle/boundule',
    'https://www.banglatribune.com/journey/travel-tour',
    'https://www.banglatribune.com/journey/aviation',
    'https://www.banglatribune.com/journey/tourism-news',
    'https://www.banglatribune.com/journey/wonder',
    'https://www.banglatribune.com/journey/hotel-resort',



    
]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Bangladesh_Tribune\\news_links.json", start_urls)