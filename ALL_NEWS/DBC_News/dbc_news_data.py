from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import json
import time, re
import html
import urllib.parse

class NewsScraper:
    
    def bengali_to_english(self, bengali_str):
        # Mapping Bengali numerals to English numerals
        bengali_to_english_digits = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        return bengali_str.translate(bengali_to_english_digits)

    def replace_bengali_strings(self, english_date_str):
        month_replacements = {
            'জানুয়ারি': 'January', 
            'ফেব্রুয়ারি': 'February',    
            'জানুয়ারী': 'January',
            'জানুয়ারী': 'January', 
            'ফেব্রুয়ারী': 'February',
            'মার্চ': 'March',
            'এপ্রিল': 'April',
            'মে': 'May',
            'জুন': 'June',
            'জুলাই': 'July',
            'আগস্ট': 'August',
            'সেপ্টেম্বর': 'September',
            'অক্টোবর': 'October',
            'নভেম্বর': 'November',
            'ডিসেম্বর': 'December'
        }
        
        # Replace Bengali day names with English ones
        day_replacements = {
            'শনিবার': 'Saturday',
            'রবিবার': 'Sunday',
            'সোমবার': 'Monday',
            'মঙ্গলবার': 'Tuesday',
            'বুধবার': 'Wednesday',
            'বৃহঃস্পতিবার': 'Thursday',
            'শুক্রবার': 'Friday'
        }

        # Replace each Bengali month name with its English equivalent
        for bengali_month, english_month in month_replacements.items():
            english_date_str = english_date_str.replace(bengali_month, english_month)

        # Replace each Bengali day name with its English equivalent
        for bengali_day, english_day in day_replacements.items():
            english_date_str = english_date_str.replace(bengali_day, english_day)

        # Replace Bengali AM/PM with English equivalents
        english_date_str = english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM').replace('অপরাহ্ন', "PM").replace('পূর্বাহ্ন', 'AM')        
        return english_date_str

    def parse_bengali_date(self, bengali_date_str):
        from datetime import datetime, timedelta
        import re

        # Remove unnecessary parts like 'প্রকাশ' or 'আপডেট' and strip extra whitespace
        bengali_date_str = bengali_date_str.replace('প্রকাশ : ', '').strip()
        bengali_date_str = bengali_date_str.replace('আপডেট : ', '').strip()
        bengali_date_str = re.sub(r'(\d+)(শে|লা|ই|রা|ঠা|লা)', r'\1', bengali_date_str)


        # Handle relative time like "২৯ মিনিট আগে"
        if "ঘন্টা আগে" in bengali_date_str or "মিনিট আগে" in bengali_date_str:
            match = re.match(r"(\d+)\s*(ঘন্টা আগে|মিনিট আগে)", bengali_date_str)
            if match:
                bengali_number = match.group(1)
                unit = match.group(2)
                english_number = int(self.bengali_to_english(bengali_number))
                current_time = datetime.now()

                if "ঘন্টা" in unit:
                    return (current_time - timedelta(hours=english_number)).replace(microsecond=0)
                elif "মিনিট" in unit:
                    return (current_time - timedelta(minutes=english_number)).replace(microsecond=0)
        # Convert Bengali numerals to English numerals
        english_date_str = self.bengali_to_english(bengali_date_str)

        # Replace Bengali strings (month/day names)
        english_date_str = self.replace_bengali_strings(english_date_str)

        # Handle any extra spaces in the time format
        english_date_str = re.sub(r'(\d{1,2}):(\d{1,2})', r'\1:\2', english_date_str)

        print(f"Final date string for parsing: {english_date_str}")  # Debugging print

        # Parse the date string into a datetime object
        try:
            return datetime.strptime(english_date_str, "%A %d %B %Y %I:%M:%S %p")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None

        

        # Parse the date with the assumed format (e.g., "23 October, 2024")
        try:
            parsed_date = datetime.strptime(english_date_str, "A %d %B %Y %I:%M, ")
            return parsed_date.replace(microsecond=0)
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None  # Handle errors as needed


    def scrape_news_data(self, url, news_type, subcategory):
        # Configure ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
        chrome_options.add_argument("--no-sandbox")  # Required for certain environments
        chrome_options.add_argument("--use-gl=swiftshader")  # Force software rendering
        chrome_options.add_argument("--disable-software-rasterizer")  # Prevent GPU fallback
        chrome_options.add_argument("--disable-webgl")  # Disable WebGL entirely
        chrome_options.add_argument("--window-size=1920,1080")  # Set window size to avoid resolution-related errors
        chrome_options.add_argument('--disable-gpu-compositing')
        chrome_options.add_argument('--disable-accelerated-2d-canvas')


        driver = webdriver.Chrome(service=Service(), options=chrome_options)

        wait = WebDriverWait(driver, 30)
        # Open the URL
        try:
            driver.get(url)
            driver.maximize_window()
            time.sleep(5)
        except:
            return
        
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        
        # Initialize the dictionary to hold the news data
        news_data = {}

        # Extract URL
        news_data['url'] = url

        # Extract title from meta tag
        try:
            title = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]').get_attribute('content')
            news_data['title'] = title
        except Exception as e:
            print(f"Error extracting title: {e}")
            news_data['title'] = None

        # Extract image URL using CSS selector
        try:
            image_url = driver.find_elements(By.XPATH, '/html/body/div[1]/main/article/div[1]/div/div/div[2]/span/img')
            image_url = image_url[0].get_attribute('src')
            news_data['image_urls'] = image_url
        except Exception as e:
            print(f"Error extracting image URL: {e}")
            news_data['image_urls'] = None

        # Extract content
        try:
            # Locate the main news article section
            content_elements = driver.find_elements(By.XPATH, '/html/body/div[1]/main/article/div[2]/div/div[1]/div[2]/div/div[2]/p')
            
            content = "\n".join([elem.text for elem in content_elements])
            
            news_data['content'] = content
    
        except Exception as e:
            print(f"Error extracting content: {e}")
            news_data['content'] = None

        # Extract author
        try:
            author_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/article/div[1]/div/div/div[1]/div[1]/div/div/p[1] | //div[@class="mx-2"]/p[@class="-mb-1 text-base font-semibold transition duration-300 "]'))
            )
            # Extract the text from the located element
            author = author_element.get_attribute('innerText').strip()
            
            print(author,"=========================author_name====================================")  # This should print "অনলাইন ডেস্ক" or the relevant author name
            news_data['author'] = author
        except Exception as e:
            print("Error fetching author:", e)
            news_data['author'] = None

        # Extract meta-description
        try:
            meta_description = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:description"]').get_attribute('content')
            
            if meta_description:
                meta_description = html.unescape(meta_description)
            news_data['meta_description'] = meta_description
        except Exception as e:
            print(f"Error extracting meta-description: {e}")
            news_data['meta_description'] = None

        # Extract keywords (hardcoded + dynamic keywords)
        # keywords = ['TCB', 'টিসিবি', 'ট্রেডিং করপোরেশন অব বাংলাদেশ (টিসিবি)']
       
        # try:
        #     # Look for additional dynamic keywords in the content
        #     content_keywords = []
        #     if any(kw in content for kw in ['টিসিবির ফ্যামিলি কার্ড', 'ফ্যামিলি কার্ড']):
        #         content_keywords.extend(['টিসিবির ফ্যামিলি কার্ড', 'ফ্যামিলি কার্ড'])
            
        #     if any(kw in content for kw in ['টিসিবির পণ্য বিক্রি', 'টিসিবির পণ্য', 'পণ্য বিক্রি']):
        #         content_keywords.extend(['টিসিবির পণ্য বিক্রি', 'টিসিবির পণ্য', 'পণ্য বিক্রি'])
            
        #     keywords.extend(content_keywords)
            
        #     # Add meta keywords if present
        #     meta_keywords = driver.find_element(By.CSS_SELECTOR, 'meta[name="keywords"]').get_attribute('content').split(',')
        #     keywords.extend(meta_keywords)
        #     # Remove duplicates
        #     news_data['keywords'] = list(set(keywords))
        # except Exception as e:
        #     print(f"Error extracting keywords: {e}")
        #     news_data['keywords'] = list(set(keywords))

        # Extract news subcategory and type
        try:
            keyword = driver.find_element(By.CSS_SELECTOR, 'meta[name="keywords"]').get_attribute('content')
            news_data['keywords'] = keyword.split(',')
        except:
            news_data['keywords'] = []
        news_data['news_subcategory'] = subcategory  # Hardcoding as per your requirement
        news_data['news_type'] = news_type  # Hardcoding as per your requirement
        news_data['media_type'] = 'Tv Media'

        # Extract published date and updated date
        try:
            published_date = driver.find_element(By.XPATH, '//span[@class="text-sm whitespace-nowrap"]')
            published_date = published_date.text
            
            # Clean the text to get the date
            published_date_text = published_date.replace("প্রকাশিত: ", "")
            
            # Parse the dates to ISO format using helper functions
            published_date = self.parse_bengali_date(published_date_text.strip())
            news_data['published_date'] = published_date.isoformat() if published_date else None
        except Exception as e:
            print(f"Error extracting dates: {e}")
            news_data['published_date'] = None
        try:
            # Click the button to update the time
            # update_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[3]/span/svg/path[1]')
            # ActionChains(driver).move_to_element(update_button).click().perform()

            # Wait for the updated content to load (if necessary, you can use WebDriverWait)
            updated_date_text = driver.find_elements(By.XPATH, '//div[@class="DPublishTime"]')
            updated_date_text = updated_date_text[1].text
            print(updated_date_text)
            updated_date_text = updated_date_text.replace("আপডেট: ", "")

            # Parse the date to ISO format
            updated_date = self.parse_bengali_date(updated_date_text.strip())
            news_data['updated_date'] = updated_date.isoformat() if updated_date else None
        except Exception as e:
            
            news_data['updated_date'] = None

        # Add the source and last_scraped time
        news_data['source'] = "ডিবিসি নিউজ"
        news_data['last_scraped'] = datetime.now().isoformat()

        # Close the browser when done
        driver.quit()

        return news_data
# scraper = NewsScraper()
# print(scraper.scrape_news_data("https://www.ittefaq.com.bd/687513/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF%E0%A6%B0-%E0%A6%9C%E0%A6%A8%E0%A7%8D%E0%A6%AF-%E0%A6%B8%E0%A7%9F%E0%A6%BE%E0%A6%AC%E0%A6%BF%E0%A6%A8-%E0%A6%A4%E0%A7%87%E0%A6%B2-%E0%A6%93-%E0%A6%AE%E0%A6%B8%E0%A7%81%E0%A6%B0-%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%95%E0%A6%BF%E0%A6%A8%E0%A6%9B%E0%A7%87-%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0"))

try:
    with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DBC_News\\dbc_news_data.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []  # Initialize empty if file doesn't exist

# Extract only new URLs not already in the file
existing_url = {item['url'] for item in existing_data if item}

# Loading unique links
with open('C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DBC_News\\sample_news_links.json', encoding = "utf-8") as f:
    d = json.load(f)

all_data = []
for i in d:
    url = i['url']
    type = i['news_type']
    subcategory = i['news_subcategory']
    scraper = NewsScraper()
    if url not in existing_url:
        print(url)
        news_data = scraper.scrape_news_data(url, type, subcategory)
        all_data.append(news_data)



# Append new data to existing data and write back to JSON
existing_data.extend(all_data)
with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DBC_News\\dbc_news_data.json", 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"Saved {len(all_data)} unique links to dailybd_data.json")
