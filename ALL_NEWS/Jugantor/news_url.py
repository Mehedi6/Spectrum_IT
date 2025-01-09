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
        elif 'government' in url:
            return ['national', 'government']
        elif 'law-justice' in url:
            return ['national', 'law-justice']
        elif 'accident' in url:
            return ['national', 'accident']
        elif 'mourning' in url:
            return ['national', 'mourning']
        elif 'national-others' in url:
            return ['national', 'others']
        elif 'media' in url:
            return ['national', 'media']
        elif 'location/dhaka' in url:
            return ['national', 'capital-city']
        elif 'location/chittagong' in url:
            return ['national', 'chittagong']
        elif 'location/Barishal' in url:
            return ['national', 'barishal']
        elif 'location/khulna' in url:
            return ['national', 'khulna']
        elif 'location/mymensingh' in url:
            return ['national', 'mymensingh']
        elif 'location/rajshahi' in url:
            return ['national', 'rajshahi']
        elif 'location/rangpur' in url:
            return ['national', 'rangpur']
        elif 'location/sylhet' in url:
            return ['national', 'sylhet']
        
        elif 'crime' in url:
            return ['crime', 'general']
        
        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'tenis' in url:
            return ['sports', 'tennis']  # Correcting spelling to 'tennis'
        elif 'interview' in url:
            return ['sports', 'interview']
        elif 'sports-others' in url:
            return ['sports', 'others']
        elif 'sports' in url:
            return ['sports', 'general']
        
        # International URLs
        elif 'northamerica' in url:
            return ['international', 'north-america']
        elif 'australian-continent' in url:
            return ['international', 'australia']
        elif 'united-states' in url:
            return ['international', 'united-states']
        elif 'united-kingdom' in url:
            return ['international', 'united-kingdom']
        elif 'middle-east' in url:
            return ['international', 'middle-east']
        elif 'asia' in url:
            return ['international', 'asia']
        elif 'europe' in url:
            return ['international', 'europe']
        elif 'pakistan' in url:
            return ['international', 'pakistan']
        elif 'malaysia' in url:
            return ['international', 'malaysia']
        elif 'india' in url:
            return ['international', 'india']
        elif 'africa' in url:
            return ['international', 'africa']
        elif 'southamerica' in url:
            return ['international', 'south-america']
        elif 'international-others' in url:
            return ['international', 'others']
        elif 'international' in url:
            return ['international', 'general']

        # Economics URLs
        elif 'budget' in url:
            return ['economics', 'budget']
        elif 'import-export' in url:
            return ['economics', 'import-export']
        elif 'garments' in url:
            return ['economics', 'garments']
        elif 'share-market' in url:
            return ['economics', 'share-market']
        elif 'bank' in url:
            return ['economics', 'bank']
        elif 'insurance' in url:
            return ['economics', 'insurance']
        elif 'tourism' in url:
            return ['economics', 'tourism']
        elif 'revenue' in url:
            return ['economics', 'revenue']
        elif 'entrepreneur' in url:
            return ['economics', 'entrepreneur']
        elif 'economics-others' in url:
            return ['economics', 'others']
        elif 'private-companies' in url:
            return ['economics', 'private-companies']
        elif 'economics' in url:
            return ['economics', 'general']
        
        # Politics URLs
        elif 'bnp' in url:
            return ['politics', 'bnp']
        elif 'awami-league' in url:
            return ['politics', 'awami-league']
        elif 'national-party' in url:
            return ['politics', 'national-party']
        elif 'politics-others' in url:
            return ['politics', 'others']
        elif 'jamaat' in url:
            return ['politics', 'jamaat']

        # Lifestyle URLs
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        elif 'recipe' in url:
            return ['lifestyle', 'recipe']
        elif 'my-family' in url:
            return ['lifestyle', 'family']
        elif 'solution' in url:
            return ['lifestyle', 'solution']
        elif 'cooking' in url:
            return ['lifestyle', 'cooking']
        elif 'beauty' in url:
            return ['lifestyle', 'beauty']
        elif 'tips' in url:
            return ['lifestyle', 'tips']
        elif 'lifestyle-others' in url:
            return ['lifestyle', 'others']
        elif 'legal-advice' in url:
            return ['lifestyle', 'legal-advice']
        
        # Entertainment URLs
        elif 'dhaliwood' in url:
            return ['entertainment', 'dhaliwood']
        elif 'bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'tollywood' in url:
            return ['entertainment', 'tollywood']
        elif 'entertainment-others' in url:
            return ['entertainment', 'others']
        elif 'song' in url:
            return ['entertainment', 'song']
        elif 'entertainment-interview' in url:
            return ['entertainment', 'interview']
        elif 'drama' in url:
            return ['entertainment', 'drama']

        # Exile section
        elif 'exile' in url:
            return ['expatriate', 'general']

        # Interviews
        elif 'interview' in url:
            return ['opinion', 'general']
        
        elif 'travel' in url:
            return ['travel', 'general']
        
        # Technology URLs
        elif 'tech' in url and 'interview' in url:
            return ['technology', 'interview']
        elif 'tech' in url:
            return ['technology', 'general']
        elif 'telco' in url:
            return ['technology', 'telecommunication']
        elif 'mobile' in url:
            return ['technology', 'mobile']
        elif 'it-social-media' in url:
            return ['technology', 'social-media']
        elif 'apps' in url:
            return ['technology', 'apps']
        elif 'invantion' in url:
            return ['technology', 'invention']
        elif 'science' in url:
            return ['technology', 'science']
        elif 'freelancing' in url:
            return ['technology', 'freelancing']
        elif 'reviews' in url:
            return ['technology', 'reviews']
        elif 'tech-others' in url:
            return ['technology', 'others']
        elif 'report' in url:
            return ['technology', 'report']

        # Campus URLs
        elif 'campus' in url and 'others' in url:
            return ['education', 'others']
        elif 'campuses' in url:
            return ['education', 'campus']
        elif 'tutorials' in url:
            return ['education', 'tutorials']
        elif 'admission' in url:
            return ['education', 'admission']
        elif 'exam' in url:
            return ['education', 'exam']
        elif 'results' in url:
            return ['education', 'results']
        elif 'scholarship' in url:
            return ['education', 'scholarship']
        elif 'study-abroad' in url:
            return ['education', 'study-abroad']

        # Job-Seeking URLs
        elif 'job-seek' in url and 'media' in url:
            return ['jobs', 'job-seek']
        elif 'job-seek' in url:
            return ['jobs', 'job-seek']
        elif 'govt-job' in url:
            return ['jobs', 'government']
        elif 'private-job' in url:
            return ['jobs', 'private']
        elif 'bank-insurance' in url:
            return ['jobs', 'bank-insurance']
        elif 'state-org' in url:
            return ['jobs', 'state-organizations']
        elif 'defence' in url:
            return ['jobs', 'defense']
        elif 'international-org' in url:
            return ['jobs', 'international-organizations']
        elif 'educational-institution' in url:
            return ['jobs', 'educational-institution']
        elif 'ngo' in url:
            return ['jobs', 'ngo']
        elif 'ecruitment-exam' in url:
            return ['jobs', 'recruitment-exam']
        elif 'recruitment-exam-prep' in url:
            return ['jobs', 'exam-preparation']
        elif 'job-seek-others' in url:
            return ['jobs', 'others']

        # Literature URLs
        elif 'literature' in url and 'interview' in url:
            return ['literature', 'interview']
        elif 'literature' in url:
            return ['literature', 'general']
        elif 'book-fair' in url:
            return ['literature', 'book-fair']
        elif 'prize' in url:
            return ['literature', 'prize']
        elif 'literature-others' in url:
            return ['literature', 'others']
        elif 'prose' in url:
            return ['literature', 'prose']
        elif 'poem' in url:
            return ['literature', 'poem']
        elif 'book-discussion' in url:
            return ['literature', 'book-discussion']
        elif 'news-of-the-art-literature' in url:
            return ['literature', 'news']
        elif 'story' in url:
            return ['literature', 'story']
        
        # Interviews
        elif 'interview' in url:
            return ['opinion', 'general']

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
                if count == 250:
                    break
                # Scroll down first to ensure the "See More" button is visible
                scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 30)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//span[@class="loadMoreButton clickLoadMoreDesktop"]')
                ))

                try:
                    # Attempt to click the button
                    see_more_button.click()
                    count+=1
                    print(f"Clicked 'See More' button. {count} time(s)")
                    
                    time.sleep(5)  # Wait for more content to load
                    # Check if new content has been loaded
                    current_article_count = len(driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div[3]/div/div/a'))  # Replace with appropriate selector for articles

                    if current_article_count == previous_article_count:
                        # Define the number of clicks
                        num_clicks = 10

                        for _ in range(num_clicks):
                            try:
                                see_more_button.click()
                                # Optional: wait for the page to load or for content to appear
                                time.sleep(3)  # You can adjust the wait time as needed (or use WebDriverWait)
                                current_article_count = len(driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div[3]/div/div/a'))  # Replace with appropriate selector for articles
                                if current_article_count != previous_article_count:
                                    print("More new contents loaded.")
                                    count+=1
                                    break
                                
                            except Exception as e:
                                print(f"Error clicking the button: {e}")
                                break  # If there's an issue (like the button not being clickable), stop the loop
                        current_article_count = len(driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[2]/div[3]/div/div/a'))  # Replace with appropriate selector for articles
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
        
        paths = ['/html/body/div[2]/div/div/div/div[3]/div[1]//div/a',
                 '/html/body/div[2]/div/div/div/div[3]/div[2]/div[3]/div/div/a',
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
                'https://www.jugantor.com/northamerica',
                'https://www.jugantor.com/australian-continent',
                'https://www.jugantor.com/united-states',
                'https://www.jugantor.com/united-kingdom',
                'https://www.jugantor.com/middle-east',
                'https://www.jugantor.com/asia',
                'https://www.jugantor.com/europe',
                'https://www.jugantor.com/pakistan',
                'https://www.jugantor.com/malaysia',
                'https://www.jugantor.com/india',
                'https://www.jugantor.com/africa',
                'https://www.jugantor.com/southamerica',
                'https://www.jugantor.com/international-others',

        
                #DONE=========================================================

                # 'https://www.jugantor.com/budget',
                # 'https://www.jugantor.com/import-export',
                # 'https://www.jugantor.com/garments',
                # 'https://www.jugantor.com/share-market',
                # 'https://www.jugantor.com/bank',
                # 'https://www.jugantor.com/insurance',
                # 'https://www.jugantor.com/tourism',
                # 'https://www.jugantor.com/revenue',
                # 'https://www.jugantor.com/entrepreneur',
                # 'https://www.jugantor.com/economics-others',
                # 'https://www.jugantor.com/private-companies',

                # 'https://www.jugantor.com/government',
                # 'https://www.jugantor.com/law-justice',
                # 'https://www.jugantor.com/location/dhaka',
                # 'https://www.jugantor.com/location/chittagong',
                # 'https://www.jugantor.com/location/Barishal',
                # 'https://www.jugantor.com/location/khulna',
                # 'https://www.jugantor.com/location/mymensingh',
                # 'https://www.jugantor.com/location/rajshahi',
                # 'https://www.jugantor.com/location/rangpur',
                # 'https://www.jugantor.com/location/sylhet',
                # 'https://www.jugantor.com/accident',
                # 'https://www.jugantor.com/mourning',
                # 'https://www.jugantor.com/national-others',
                # 'https://www.jugantor.com/media',

                # 'https://www.jugantor.com/crime',

                # 'https://www.jugantor.com/jamaat',
                # 'https://www.jugantor.com/bnp',
                # 'https://www.jugantor.com/awami-league',
                # 'https://www.jugantor.com/national-party',
                # 'https://www.jugantor.com/politics-others',

                #=============================================================
            
                # 'https://www.jugantor.com/cricket',
                # 'https://www.jugantor.com/football',
                # 'https://www.jugantor.com/tenis',
                # 'https://www.jugantor.com/interview',
                # 'https://www.jugantor.com/sports-others',
                # 'https://www.jugantor.com/sports',
            
            
            
                # 'https://www.jugantor.com/lifestyle',
                # 'https://www.jugantor.com/recipe',
                # 'https://www.jugantor.com/my-family',
                # 'https://www.jugantor.com/solution',
                # 'https://www.jugantor.com/cooking',
                # 'https://www.jugantor.com/beauty',
                # 'https://www.jugantor.com/tips',
                # 'https://www.jugantor.com/lifestyle-others',
                # 'https://www.jugantor.com/news',
                # 'https://www.jugantor.com/legal-advice',

                # 'https://www.jugantor.com/travel',

                # 'https://www.jugantor.com/exile'
           
                # 'https://www.jugantor.com/dhaliwood',
                # 'https://www.jugantor.com/bollywood',
                # 'https://www.jugantor.com/hollywood',
                # 'https://www.jugantor.com/entertainment-others',
                # 'https://www.jugantor.com/tollywood',
                # 'https://www.jugantor.com/song',
                # 'https://www.jugantor.com/entertainment-interview',
                # 'https://www.jugantor.com/drama',
        
                # 'https://www.jugantor.com/interview',
            
                # 'https://www.jugantor.com/tech',
                # 'https://www.jugantor.com/telco',
                # 'https://www.jugantor.com/mobile',
                # 'https://www.jugantor.com/it-social-media',
                # 'https://www.jugantor.com/apps',
                # 'https://www.jugantor.com/invantion',
                # 'https://www.jugantor.com/science',
                # 'https://www.jugantor.com/freelancing',
                # 'https://www.jugantor.com/reviews',
                # 'https://www.jugantor.com/tech-others',
                # 'https://www.jugantor.com/report',
                # 'https://www.jugantor.com/tech-interview'

                #================================================
                # 'https://www.jugantor.com/tutorials',
                # 'https://www.jugantor.com/admission',
                # 'https://www.jugantor.com/exam',
                # 'https://www.jugantor.com/results',
                # 'https://www.jugantor.com/scholarship',
                # 'https://www.jugantor.com/campuses',
                # 'https://www.jugantor.com/study-abroad',
                # 'https://www.jugantor.com/campus-others',
            
                # 'https://www.jugantor.com/job-seek',
                # 'https://www.jugantor.com/govt-job',
                # 'https://www.jugantor.com/private-job',
                # 'https://www.jugantor.com/bank-insurance',
                # 'https://www.jugantor.com/state-org',
                # 'https://www.jugantor.com/defence',
                # 'https://www.jugantor.com/nternational-org',
                # 'https://www.jugantor.com/educational-institution',
                # 'https://www.jugantor.com/ngo',
                # 'https://www.jugantor.com/job-seek-media',
                # 'https://www.jugantor.com/ecruitment-exam',
                # 'https://www.jugantor.com/recruitment-exam-prep',
                # 'https://www.jugantor.com/job-seek-others',
                #=============================================================
            
                # 'https://www.jugantor.com/literature',
                # 'https://www.jugantor.com/book-fair',
                # 'https://www.jugantor.com/prize',
                # 'https://www.jugantor.com/literature-others',
                # 'https://www.jugantor.com/prose',
                # 'https://www.jugantor.com/poem',
                # 'https://www.jugantor.com/literature-interview',
                # 'https://www.jugantor.com/book-discussion',
                # 'https://www.jugantor.com/news-of-the-art-literature',
                # 'https://www.jugantor.com/story',


]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Jugantor\\news_links.json", start_urls)
