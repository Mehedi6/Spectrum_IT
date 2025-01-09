# ittefaq_tcb_link_collector.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time, json
import html
import urllib.parse

# Function to scrape the given URLs and save the output links to a JSON file
def scrape_links(output_file_name, urls_to_scrape):
    # Configure ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    
    #Get the News Type
    def get_news_type(url):
        if 'national' in url:
            return ['national', 'general']
        elif 'রাজধানীর-খবর' in url:
            return ['national', 'capital-city']
        elif 'জাতীয়-সংসদ' in url:
            return ['natinal', 'parliament-news']
        elif 'চট্টগ্রামের-খবর' in url:
            return ['national', 'chittagong-city']
        elif "politics" in url:
            return ['politics', 'general']
        elif 'জাতীয়-পার্টি' in url:
            return ['politics', 'জাতীয়-পার্টি']
        elif 'আওয়ামী-লীগ' in url:
            return ['politics', 'আওয়ামী-লীগ']
        elif 'বিএনপি' in url:
            return ['politics', 'বিএনপি']
        elif 'economy/bank' in url:
            return ['economics', 'bank']
        elif 'economy/insurance' in url:
            return ['economics', 'insurance']
        elif 'economy/stock-market' in url:
            return ['economics', 'stock-market']
        elif 'বাজার-দর' in url:
            return ['economics', 'market']
        elif 'বাজেট' in url:
            return ['economics', 'budget']
        elif '/economy' in url:
            return ['economics', 'general']
        elif 'মধ্যপ্রাচ্য' in url:
            return ['international', 'middle-east']
        elif 'ভারত' in url:
            return ['international', 'india']
        elif 'পাকিস্তান' in url:
            return ['international', 'pakistan']
        elif 'কাশ্মীর' in url:
            return ['international', 'kashmir']
        elif 'চীন' in url:
            return ['international', 'china']
        elif 'আফ্রিকা' in url:
            return ['international', 'africa']
        elif 'এশিয়া' in url:
            return ['international', 'asia']
        elif 'ইউরোপ' in url:
            return ['international', 'europe']
        elif 'আমেরিকা' in url:
            return ['international', 'america']
        elif 'sports/cricket' in url:
            return ['sports', 'cricket']
        elif 'sports/football' in url:
            return ['sports', 'football']
        elif 'sports/hockey' in url:
            return ['sports', 'hockey']
        elif 'sports/others' in url:
            return ['sports', 'others']
        elif 'entertainment/bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'entertainment/hollywood' in url:
            return['entertainment', 'hollywood']
        elif 'entertainment/dhallywood' in url:
            return ['entertainment', 'dhallywood']
        
        elif 'সরকারি-চাকরি' in url:
            return ['jobs', 'govt-job']
        elif 'ক্যারিয়ার-পরামর্শ' in url:
            return ['jobs', 'career-advise']
        elif 'এনজিওতে-নিয়োগ' in url:
            return ['jobs', 'ngo-circular']
        elif 'বেসরকারি-চাকরি' in url:
            return ['jobs', 'private-job']
        elif 'পার্টটাইম-চাকরি' in url:
            return ['jobs', 'part-time']
        elif 'চাকরির-খবর' in url:
            return ['jobs', 'job-news']
        
        elif 'health' in url:
            return ['health', 'general']
        elif 'স্বাস্থ্য-পরামর্শ' in url:
            return ['health', 'health-tips']
        elif 'law-courts' in url:
            return ['national', 'law-courts']
        elif 'টিপস' in url:
            return ['lifestyle', 'tips']
        elif 'রূপচর্চা' in url or 'মেকআপ' in url:
            return ['lifestyle', 'makeup']
        elif 'রেসিপি' in url:
            return ['lifestyle', 'recipe']
        elif 'সম্পর্ক' in url:
            return ['lifestyle', 'relation']
        elif 'শিশু' in url:
            return ['lifestyle', 'children']
        
        elif 'technology' in url:
            return ['technology', 'general']
        elif 'বিজ্ঞান-ও-আবিষ্কার' in url:
            return ['science', 'science-invention']
        elif 'স্মার্টফোন' in url:
            return ['technology', 'smartphone']
        
        elif 'tourism' in url:
            return ['travel', 'general']
        
        elif 'education' in url:
            return ['education', 'general']
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'probash' in url:
            return ['expatriate', 'general']
        elif 'opinion' in url:
            return ['opinion', 'general']
        else:
            return ['general', 'general']
         
        
       
        
        

        
        
        

    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling
    
    # Click the "See More" button until it no longer appears
    def click_see_more_button():
        count = 0
        while True:
            try:
                if count == 5:
                    break
                # Scroll down first to ensure the "See More" button is visible
                scroll_down()

                # Wait for the button to be clickable
                wait = WebDriverWait(driver, 10)
                see_more_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//button[@class="text-white text-lg bg-[var(--brand-color)] px-4 py-2 flex items-center justify-center hover:bg-[var(--button-hover)] rounded-sm"]')
                ))

                try:
                    # Attempt to click the button
                    see_more_button.click()
                    count+=1
                    print("Clicked 'See More' button.")
                    time.sleep(2)  # Wait for more content to load
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
    # Extract links from both types of card elements
    # Function to extract links from both types of card elements
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        card_elements = driver.find_elements(By.XPATH,'//div[@class="col-span-12 md:col-span-6 relative"]/a | /html/body/main/section/div/div[2]/div[1]/a | //div[@class="flex flex-col pb-6"]/div/a')
     
        
        
        print(len(card_elements))
        for card in card_elements:
            link = card.get_attribute('href')
            if link:
                links.add(link)

        return links  # Return the unique links as a set

    # Collect all unique links across all pages
    all_links = set()
    
    for url in urls_to_scrape:
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        # Step 1: Click all "See More" buttons
        click_see_more_button()
        url = urllib.parse.unquote(url)
        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        news_type, news_subcategory = get_news_type(url)
        # all_links.update(links_data)  # Update the set to ensure all links are unique
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

    print(f"Saved {len(filtered_new_data)} unique links to {output_file_name}")
    
    # Close the browser when done
    driver.quit()

news_links = ["https://www.dhakapost.com/national",
              "https://www.dhakapost.com/topic/%E0%A6%B0%E0%A6%BE%E0%A6%9C%E0%A6%A7%E0%A6%BE%E0%A6%A8%E0%A7%80%E0%A6%B0-%E0%A6%96%E0%A6%AC%E0%A6%B0",
              "https://www.dhakapost.com/topic/%E0%A6%9C%E0%A6%BE%E0%A6%A4%E0%A7%80%E0%A7%9F-%E0%A6%B8%E0%A6%82%E0%A6%B8%E0%A6%A6",
              "https://www.dhakapost.com/topic/%E0%A6%9A%E0%A6%9F%E0%A7%8D%E0%A6%9F%E0%A6%97%E0%A7%8D%E0%A6%B0%E0%A6%BE%E0%A6%AE%E0%A7%87%E0%A6%B0-%E0%A6%96%E0%A6%AC%E0%A6%B0",
              "https://www.dhakapost.com/politics",
              "https://www.dhakapost.com/topic/%E0%A6%86%E0%A6%93%E0%A7%9F%E0%A6%BE%E0%A6%AE%E0%A7%80-%E0%A6%B2%E0%A7%80%E0%A6%97",
              "https://www.dhakapost.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%8F%E0%A6%A8%E0%A6%AA%E0%A6%BF",
              "https://www.dhakapost.com/topic/%E0%A6%9C%E0%A6%BE%E0%A6%A4%E0%A7%80%E0%A7%9F-%E0%A6%AA%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%9F%E0%A6%BF",
              "https://www.dhakapost.com/economy",
              'https://www.dhakapost.com/economy/bank',
              'https://www.dhakapost.com/economy/insurance',
              'https://www.dhakapost.com/economy/stock-market',
              'https://www.dhakapost.com/topic/%E0%A6%AC%E0%A6%BE%E0%A6%9C%E0%A6%BE%E0%A6%B0-%E0%A6%A6%E0%A6%B0',
              'https://www.dhakapost.com/topic/%E0%A6%AC%E0%A6%BE%E0%A6%9C%E0%A7%87%E0%A6%9F',
              
              'https://www.dhakapost.com/topic/%E0%A6%AE%E0%A6%A7%E0%A7%8D%E0%A6%AF%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%BE%E0%A6%9A%E0%A7%8D%E0%A6%AF',
              'https://www.dhakapost.com/topic/%E0%A6%AD%E0%A6%BE%E0%A6%B0%E0%A6%A4',
              'https://www.dhakapost.com/topic/%E0%A6%AA%E0%A6%BE%E0%A6%95%E0%A6%BF%E0%A6%B8%E0%A7%8D%E0%A6%A4%E0%A6%BE%E0%A6%A8',
              'https://www.dhakapost.com/topic/%E0%A6%95%E0%A6%BE%E0%A6%B6%E0%A7%8D%E0%A6%AE%E0%A7%80%E0%A6%B0',
              'https://www.dhakapost.com/topic/%E0%A6%9A%E0%A7%80%E0%A6%A8',
              'https://www.dhakapost.com/topic/%E0%A6%86%E0%A6%AB%E0%A7%8D%E0%A6%B0%E0%A6%BF%E0%A6%95%E0%A6%BE',
              'https://www.dhakapost.com/topic/%E0%A6%8F%E0%A6%B6%E0%A6%BF%E0%A7%9F%E0%A6%BE',
              'https://www.dhakapost.com/topic/%E0%A6%87%E0%A6%89%E0%A6%B0%E0%A7%8B%E0%A6%AA',
              'https://www.dhakapost.com/topic/%E0%A6%86%E0%A6%AE%E0%A7%87%E0%A6%B0%E0%A6%BF%E0%A6%95%E0%A6%BE',

              'https://www.dhakapost.com/sports/cricket',
              'https://www.dhakapost.com/sports/football',
              'https://www.dhakapost.com/sports/hockey',
              'https://www.dhakapost.com/sports/others',

              'https://www.dhakapost.com/entertainment/bollywood',
              'https://www.dhakapost.com/entertainment/hollywood',
              'https://www.dhakapost.com/entertainment/dhallywood',

              'https://www.dhakapost.com/topic/%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0%E0%A6%BF-%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF',
              'https://www.dhakapost.com/topic/%E0%A6%95%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%B0%E0%A6%BF%E0%A7%9F%E0%A6%BE%E0%A6%B0-%E0%A6%AA%E0%A6%B0%E0%A6%BE%E0%A6%AE%E0%A6%B0%E0%A7%8D%E0%A6%B6',
              'https://www.dhakapost.com/topic/%E0%A6%8F%E0%A6%A8%E0%A6%9C%E0%A6%BF%E0%A6%93%E0%A6%A4%E0%A7%87-%E0%A6%A8%E0%A6%BF%E0%A7%9F%E0%A7%8B%E0%A6%97',
              'https://www.dhakapost.com/topic/%E0%A6%AC%E0%A7%87%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0%E0%A6%BF-%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF',
              'https://www.dhakapost.com/topic/%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF%E0%A6%B0-%E0%A6%96%E0%A6%AC%E0%A6%B0',
              'https://www.dhakapost.com/topic/%E0%A6%AA%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%9F%E0%A6%9F%E0%A6%BE%E0%A6%87%E0%A6%AE-%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF',
              'https://www.dhakapost.com/topic/%E0%A6%85%E0%A6%AD%E0%A6%BF%E0%A6%9C%E0%A7%8D%E0%A6%9E%E0%A6%A4%E0%A6%BE-%E0%A6%9B%E0%A6%BE%E0%A6%A1%E0%A6%BC%E0%A6%BE-%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF',
              
              'https://www.dhakapost.com/health',
              'https://www.dhakapost.com/topic/%E0%A6%B8%E0%A7%8D%E0%A6%AC%E0%A6%BE%E0%A6%B8%E0%A7%8D%E0%A6%A5%E0%A7%8D%E0%A6%AF-%E0%A6%AA%E0%A6%B0%E0%A6%BE%E0%A6%AE%E0%A6%B0%E0%A7%8D%E0%A6%B6',

              'https://www.dhakapost.com/topic/%E0%A6%9F%E0%A6%BF%E0%A6%AA%E0%A6%B8',
              'https://www.dhakapost.com/topic/%E0%A6%B0%E0%A7%82%E0%A6%AA%E0%A6%9A%E0%A6%B0%E0%A7%8D%E0%A6%9A%E0%A6%BE',
              'https://www.dhakapost.com/topic/%E0%A6%AE%E0%A7%87%E0%A6%95%E0%A6%86%E0%A6%AA',
              'https://www.dhakapost.com/topic/%E0%A6%B0%E0%A7%87%E0%A6%B8%E0%A6%BF%E0%A6%AA%E0%A6%BF',
              'https://www.dhakapost.com/topic/%E0%A6%B8%E0%A6%AE%E0%A7%8D%E0%A6%AA%E0%A6%B0%E0%A7%8D%E0%A6%95',
              'https://www.dhakapost.com/topic/%E0%A6%B6%E0%A6%BF%E0%A6%B6%E0%A7%81',

              'https://www.dhakapost.com/technology',
              'https://www.dhakapost.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%9C%E0%A7%8D%E0%A6%9E%E0%A6%BE%E0%A6%A8-%E0%A6%93-%E0%A6%86%E0%A6%AC%E0%A6%BF%E0%A6%B7%E0%A7%8D%E0%A6%95%E0%A6%BE%E0%A6%B0',
              'https://www.dhakapost.com/topic/%E0%A6%B8%E0%A7%8D%E0%A6%AE%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%9F%E0%A6%AB%E0%A7%8B%E0%A6%A8',

              'https://www.dhakapost.com/tourism',
              'https://www.dhakapost.com/education',
              'https://www.dhakapost.com/campus',
              'https://www.dhakapost.com/probash',
              'https://www.dhakapost.com/opinion',
              'https://www.dhakapost.com/law-courts',
              
              ]



scrape_links("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Dhaka_Post\\news_links.json", news_links)  
