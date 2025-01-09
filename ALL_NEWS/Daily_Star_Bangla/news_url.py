# Function to scrape the given URLs and save the output links to a JSON file
def scrape_links(output_file_name, urls_to_scrape):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

    import time, json
    import urllib.parse
    from datetime import datetime

    # Configure ChromeDriver
    chrome_options = Options()
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
    chrome_options.add_argument("--disable-3d-apis")


    # Optional: Set a realistic user-agent to mimic a real browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/116.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)


    def get_news_type(url):
        if 'bangladesh' in url:
            return ['national', 'all-bangladesh']
        elif 'crime-justice' in url:
            return ['crime', 'crime-justice']
            
        
        # International
        elif 'international' in url:
            return ['international', 'general']

        
        else:
            return ['others', 'others']
    
    # Scroll down the page a limited number of times
    def scroll_down():
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for content to load after scrolling
    def click_see_more_button():
        count = 0
        while True:
            try:
                # Gradual scrolling to ensure visibility
                scroll_down()  # Replace this with your scrolling logic if needed

                # Wait for any of the specified buttons to become clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[5]/div/div/div[1]/div/div[2]/ul/li/a | /html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[9]/div/div/div[1]/div/div[2]/ul/li/a | /html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[7]/div/div/div[1]/div/div[2]/ul/li/a | /html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[3]/div/div/div[1]/div/div[2]/ul/li/a')
                ))

                try:
                    if count >= 16000:  # Limit the number of clicks
                        print("Reached the maximum click limit.")
                        break

                    # Attempt to click the button
                    see_more_button.click()
                    print(f"Clicked 'See More' button. {count + 1} time(s)")
                    count += 1
                    time.sleep(1)  # Wait for the content to load after each click

                except ElementClickInterceptedException:
                    # If click is intercepted, retry after scrolling a bit more
                    print("Click intercepted, retrying...")
                    scroll_down()
                    continue

            except (TimeoutException, NoSuchElementException):
                # Handle cases where the button is no longer found
                print("No more 'See More' button found.")
                break

            except StaleElementReferenceException:
                # Re-locate the button if it becomes stale
                print("Stale element encountered, re-fetching the button...")
                continue


    # Extract links from loaded content
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        # Find card elements containing news links
        paths = ['//div[@class="columns small-12 medium-3 large-3"]/div/div/h3',
                 '/html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[3]/div/div/div[1]/div/div[1]/div/div[2]/h3',
                 '/html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[5]/div/div/div[1]/div/div[1]/div/div[2]/h3',
                 '/html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[7]/div/div/div[1]/div/div[1]/div/div[2]/h3',
                 '/html/body/div[3]/div[2]/div/div/div[2]/main/div/div[2]/div/div[9]/div/div/div[1]/div/div[1]/div/div[2]/h3',
                ]
        # Loop through each XPath and extract links
        for path in paths:
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, path))
                )
                card_elements = driver.find_elements(By.XPATH, path)
                print(f"Found {len(card_elements)} elements for path: {path}")

                for card in card_elements:
                    # Extract the link from <a> tag
                    
                    try:
                        # Log the card HTML for debugging
                        link_element = card.find_element(By.TAG_NAME, "a")
                        
                        link = link_element.get_attribute("href")  # Extract the href attribute
                        
                    except Exception as e:
                        print(f"Error extracting links {e}")
                        link = None  # If no link is found, set to None
                
                    if link:
                        links.add((link))  # Add link to the set to avoid duplicates
                        
            except Exception as e:
                print(f"Error extracting links for path {path}: {e}")


        return links  # Return unique links
    
    #backup the jsons
    # import shutil

    # backup_file_name = output_file_name + ".bak"
    # shutil.copy(output_file_name, backup_file_name)

    # Collect all unique links across all pages
    for url in urls_to_scrape:
        all_links = set()
        url = urllib.parse.unquote(url)
        print(f"Processing: {url}")
        
        driver.get(url)
        driver.maximize_window()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        news_type, news_subcategory = get_news_type(url)
        click_see_more_button()

        links_data = extract_links()
        if not links_data:
            print("No links found on this page.")
            continue

        for link in links_data:
            if link not in {item[0] for item in all_links}:
                all_links.add((link, news_type, news_subcategory))

        unique_links = [{"url": link[0], "news_type": link[1], "news_subcategory": link[2]} for link in all_links]

        try:
            with open(output_file_name, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_urls = {item['url'] for item in existing_data}
        filtered_new_data = [item for item in unique_links if item['url'] not in existing_urls]

        if not filtered_new_data:
            print("No new data to append.")
            continue

        existing_data.extend(filtered_new_data)

        with open(output_file_name, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4)


        print(f"Saved {len(filtered_new_data)} new links to {output_file_name}")

    # Close the browser when done
    driver.quit()

# Example usage:
start_urls = [
    
    # 'https://bangla.thedailystar.net/news/bangladesh/politics',
    # 'https://bangla.thedailystar.net/international',
    # 'https://bangla.thedailystar.net/news/bangladesh/crime-justice',
    # 'https://bangla.thedailystar.net/economy'

    # 'https://bangla.thedailystar.net/news/chattogram',
    # 'https://bangla.thedailystar.net/news/bangladesh/election',
    # 'https://bangla.thedailystar.net/news/bangladesh/agriculture',
    'https://bangla.thedailystar.net/news/bangladesh',
    # 'https://bangla.thedailystar.net/news/asia',
    # 'https://bangla.thedailystar.net/opinion',
    # 'https://bangla.thedailystar.net/health/health-care',
    # 'https://bangla.thedailystar.net/health/disease',

    # 'https://bangla.thedailystar.net/business/budget-2024-25',
    # 'https://bangla.thedailystar.net/business/budget-2022-23',
    # 'https://bangla.thedailystar.net/news/world',
    # 'https://bangla.thedailystar.net/economy/daily-commodity-price',

    #sports
    # 'https://bangla.thedailystar.net/sports/cricket',
    # 'https://bangla.thedailystar.net/sports/football',
    # 'https://bangla.thedailystar.net/sports/other-sports',
    # 'https://bangla.thedailystar.net/sports/misc',

    #entertainment
    # 'https://bangla.thedailystar.net/entertainment/%E0%A6%93%E0%A6%9F%E0%A6%BF%E0%A6%9F%E0%A6%BF',
    # 'https://bangla.thedailystar.net/entertainment/tv-movies',
    # 'https://bangla.thedailystar.net/entertainment/stage-music',
    # 'https://bangla.thedailystar.net/entertainment/music',
    # 'https://bangla.thedailystar.net/entertainment/others',

    # #Lifestyle
    # 'https://bangla.thedailystar.net/life-living/food-recipe',
    # 'https://bangla.thedailystar.net/life-living/baby-care-baby-growing',
    # 'https://bangla.thedailystar.net/life-living/relation-family',
    # 'https://bangla.thedailystar.net/life-living/wellness',
    # 'https://bangla.thedailystar.net/life-living/fashion-beauty',
    
    # #travel
    # 'https://bangla.thedailystar.net/life-living/travel',

    #Literature
    # 'https://bangla.thedailystar.net/literature/history-tradition',
    # 'https://bangla.thedailystar.net/literature/art',
    # 'https://bangla.thedailystar.net/literature/culture',
    # 'https://bangla.thedailystar.net/literature/story-poem',
    # 'https://bangla.thedailystar.net/literature/books',
    # 'https://bangla.thedailystar.net/literature/interview',

    #Education
    # 'https://bangla.thedailystar.net/youth/education',
    # 'https://bangla.thedailystar.net/youth/education/campus',
    
    
    # #jobs
    # 'https://bangla.thedailystar.net/youth/career/job',
    # 'https://bangla.thedailystar.net/youth/career/govt-job',

    # #youth
    # 'https://bangla.thedailystar.net/youth/triumph-of-youth',
    # 'https://bangla.thedailystar.net/youth/inspiration',
    # 'https://bangla.thedailystar.net/youth/initiative',
    # 'https://bangla.thedailystar.net/youth/education/student-politics-others',

    #technology
    # 'https://bangla.thedailystar.net/tech-startup/automobile',
    # 'https://bangla.thedailystar.net/tech-startup/science-tech-gadgets',
    # 'https://bangla.thedailystar.net/tech-startup/startup',
    
    # #expatriate
    # 'https://bangla.thedailystar.net/abroad/migration',
    # 'https://bangla.thedailystar.net/abroad/immigration'
    




    
]

scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ALL_NEWS\\Daily_Star_Bangla\\final_news_links.json", start_urls)
