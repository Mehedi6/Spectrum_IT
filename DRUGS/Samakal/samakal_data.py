from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import time, re
import html

class NewsScraper:
    
    def bengali_to_english(self, bengali_str):
        # Mapping Bengali numerals to English numerals
        bengali_to_english_digits = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        return bengali_str.translate(bengali_to_english_digits)

    def replace_bengali_strings(self, english_date_str):
        # Replace Bengali month names with English ones
        month_replacements = {
            'জানুয়ারি': 'January', 
            'ফেব্রুয়ারি': 'February',    
            'জানুয়ারী': 'January',
            'জানুয়ারি': 'January',
            'ফেব্রুয়ারী': 'February',
            'ফেব্রুয়ারি': 'February',
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
            'বৃহস্পতিবার': 'Thursday',
            'শুক্রবার': 'Friday'
        }

        # Replace each Bengali month name with its English equivalent
        for bengali_month, english_month in month_replacements.items():
            english_date_str = english_date_str.replace(bengali_month, english_month)

        # Replace each Bengali day name with its English equivalent
        for bengali_day, english_day in day_replacements.items():
            english_date_str = english_date_str.replace(bengali_day, english_day)

        # Replace Bengali AM/PM with English equivalents
        english_date_str = english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM')
        
        return english_date_str

    def parse_bengali_date(self, bengali_date_str):
        # Remove the 'প্রকাশ' part and strip any extra whitespace
        bengali_date_str = bengali_date_str.replace('প্রকাশ: ', '').strip()
        bengali_date_str = bengali_date_str.replace('আপডেট: ', '').strip()
        bengali_date_str = bengali_date_str.replace('টা','').strip()
        bengali_date_str = bengali_date_str.replace('|','').strip()
        
        # Convert Bengali numbers to English
        english_date_str = self.bengali_to_english(bengali_date_str)
        
        # Replace Bengali month names with English ones
        english_date_str = self.replace_bengali_strings(english_date_str)
        
        # Handle the case with the extra space in the time part
        english_date_str = re.sub(r'(\d{1,2}):(\d{1,2})', r'\1:\2', english_date_str)  # Fix extra space in time
        
        print(f"Final date string for parsing: {english_date_str}")  # Debugging print
        
        # Define the format for parsing (using 24-hour format)
        try:
            if "." in english_date_str:
                return datetime.strptime(english_date_str, "%d.%m.%Y %I:%M %p")
            # Check if the format contains a day name (e.g., "Sunday")
            elif english_date_str[0].isalpha():  
                return datetime.strptime(english_date_str, "%A, %d %B, %Y %H:%M")
            else:
                try:
                    # Try the 12-hour format first
                    return datetime.strptime(english_date_str, "%d %B %Y %H:%M")
                except ValueError:
                    # If it fails, try the 24-hour format
                    return datetime.strptime(english_date_str, "%H:%M, %A, %d %B, %Y")

        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None  # or handle error accordingly
        


    def scrape_news_data(self, url, news_type, news_subcategory):
        # Configure ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Run in headless mode
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

        # Open the URL
        try:
            driver.get(url)
            driver.maximize_window()
            time.sleep(5)
        except:
            return None
        
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
            image_url = driver.find_elements(By.XPATH, '/html/body/main/section/div/div[2]/div[1]/div[3]/img')
            image_url = image_url[0].get_attribute('src')
            news_data['image_urls'] = image_url
        except Exception as e:
            print(f"Error extracting image URL: {e}")
            news_data['image_urls'] = None

        # Extract content
        try:
            content_element = driver.find_elements(By.CSS_SELECTOR, "#contentDetails > p")
            content = "\n".join([elem.text for elem in content_element])
            
            news_data['content'] = content
    
        except Exception as e:
            print(f"Error extracting content: {e}")
            news_data['content'] = None

        # Extract author
        try:
            author_element = driver.find_element(By.XPATH, '/html/body/main/section/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/p')
            news_data['author'] = author_element.text.strip()
        except Exception as e:
            print(f"Error extracting author: {e}")
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
        keywords = ['মাদক']
        try:
            # Look for additional dynamic keywords in the content
            content_keywords = []
            if any(kw in content for kw in ['বেপরোয়া', 'কারাদণ্ড', 'ইয়াবা']):
                content_keywords.extend(['বেপরোয়া', 'কারাদণ্ড', 'ইয়াবা'])
            
            # if any(kw in content for kw in ['টিসিবির পণ্য বিক্রি', 'টিসিবির পণ্য', 'পণ্য বিক্রি']):
            #     content_keywords.extend(['টিসিবির পণ্য বিক্রি', 'টিসিবির পণ্য', 'পণ্য বিক্রি'])
            
            keywords.extend(content_keywords)
            
            # Add meta keywords if present
            try:
                meta_keywords = driver.find_element(By.CSS_SELECTOR, 'meta[name="keywords"]').get_attribute('content').split(',')
                keywords.extend(meta_keywords)
            # Remove duplicates
            except:
                pass
            news_data['keywords'] = list(set(keywords))
    
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            news_data['keywords'] = list(set(keywords))

        # Extract news subcategory and type
        news_data['news_subcategory'] = news_subcategory  # Hardcoding as per your requirement
        news_data['news_type'] = news_type  # Hardcoding as per your requirement 
        news_data['media_type'] = 'Newspaper'

        # Published Date
        try:
            # Example of simplified CSS selectors targeting key attributes
            published_date_element = driver.find_element(By.CSS_SELECTOR, 'body > main > section > div > div:nth-child(2) > div.col-lg-9 > div:nth-child(5) > div.col-lg-6.d-flex > div > div.dateAndTime > p')
            published_date = published_date_element.text

            index = published_date.find('আপডেট:')

            # Extract the substring after 'প্রকাশিত:'
            if index != -1:
                published_date_text = published_date[:index].strip()
            else:
                published_date_text = published_date 
            
            # Parse the dates to ISO format using helper functions
            published_date = self.parse_bengali_date(published_date_text.strip())
            news_data['published_date'] = published_date.isoformat() if published_date else None
        except Exception as e:
            print(f"Error extracting dates: {e}")
            news_data['published_date'] = None

        # Updated Date
        try:
            updated_date_element = driver.find_element(By.CSS_SELECTOR, 'body > main > section > div > div:nth-child(2) > div.col-lg-9 > div:nth-child(5) > div.col-lg-6.d-flex > div > div.dateAndTime > p')
            updated_date = updated_date_element.text
            # updated_date = re.sub(r'\s+', ' ', updated_date.replace("আপডেট:", "")).strip()
            index = updated_date.find('আপডেট:')

            # Extract the substring after 'প্রকাশিত:'
            if index != -1:
                updated_date_text = updated_date[index + len('আপডেট: '):].strip()
            else:
                updated_date_text = updated_date

            # Parse the dates to ISO format using helper functions
            updated_date = self.parse_bengali_date(updated_date_text.strip()) 
            news_data['updated_date'] = updated_date.isoformat() if updated_date else None 
        except Exception as e:
            print(f"Error extracting dates {e}")
            news_data['updated_date'] = None
        

        # Add the source and last_scraped time
        news_data['source'] = "সমকাল"
        news_data['last_scraped'] = datetime.now().isoformat()

        # Close the browser when done
        driver.quit()

        return news_data
# scraper = NewsScraper()
# print(scraper.scrape_news_data("https://www.ittefaq.com.bd/687513/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF%E0%A6%B0-%E0%A6%9C%E0%A6%A8%E0%A7%8D%E0%A6%AF-%E0%A6%B8%E0%A7%9F%E0%A6%BE%E0%A6%AC%E0%A6%BF%E0%A6%A8-%E0%A6%A4%E0%A7%87%E0%A6%B2-%E0%A6%93-%E0%A6%AE%E0%A6%B8%E0%A7%81%E0%A6%B0-%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%95%E0%A6%BF%E0%A6%A8%E0%A6%9B%E0%A7%87-%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0"))

# Loading unique links

try:
    with open("C:\\Users\\arwen\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Samakal\\samakal_data.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except:
    existing_data = []


# Extract only new URLs not already in the file

existing_urls = {item['url'] for item in existing_data}

with open('C:\\Users\\arwen\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Samakal\\news_links.json', encoding='utf-8') as f:
    d = json.load(f)

all_data = []
for entry in d:
    url, news_type, sub_category = entry['url'], 'crime', 'drugs'
    if url not in existing_urls:
        scraper = NewsScraper()
        news_item = scraper.scrape_news_data(url, news_type, sub_category)
        if news_item:  # Ensure published_date exists
            # Convert ISO string to datetime object
            all_data.append(news_item)
            
 

# filtered_new_data = [item for item in all_data if item['url'] not in existing_url]

# Append new data to existing data and write back to JSON
existing_data.extend(all_data)
with open("C:\\Users\\arwen\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Samakal\\samakal_data.json", 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"Saved {len(all_data)} unique links to tcb_data.json")
