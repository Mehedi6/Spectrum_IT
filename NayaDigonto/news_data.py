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
            'জানুয়ারি': 'January',
            'ফেব্রুয়ারি': 'February',
            'জানুয়ারী': 'January',
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
        # Remove unnecessary parts of the date string
        bengali_date_str = bengali_date_str.split('|')[0].strip()  # Take only the part before the '|'
        # Remove the 'প্রকাশ' part and strip any extra whitespace
        bengali_date_str = bengali_date_str.replace('প্রকাশ: ', '').strip()
        bengali_date_str = re.sub(r'\(ভিজিট\s*:\s*\d+\)', '', bengali_date_str).strip()
        
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
                return datetime.strptime(english_date_str, "%A, %d %B, %Y, %I:%M %p")
            else:
                return datetime.strptime(english_date_str, "%d %B %Y, %H:%M")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None  # Handle error accordingly if parsing fails
            


    def scrape_news_data(self, url, news_type, subcategory):
        # Configure ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(), options=chrome_options)

        # Open the URL
        try:
            driver.get(url)
            time.sleep(1)
        except Exception as e:
            print(f"Error parsing: {e}")
            return
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
            image_url = driver.find_elements(By.XPATH, '//*[@id="adf-overlay"]')
            image_url = image_url[0].get_attribute('src')
            news_data['image_urls'] = image_url
        except Exception as e:
            print(f"Error extracting image URL: {e}")
            news_data['image_urls'] = None

        # Extract content
        try:
            # Locate the main news article section
            main_content_section = driver.find_elements(By.CSS_SELECTOR, 'body > div.main.detail > div > div > div > div:nth-child(3) > div.col-md-8 > div.news-content > p')
            
            # # Gather paragraphs from both .mb-5 and .my-5 article classes within the main content
            # mb5_elements = main_content_section.find_elements(By.CSS_SELECTOR, "article.mb-5 > p")
            # # my5_elements_1 = main_content_section.find_elements(By.CSS_SELECTOR, "article.my-5")
            # my5_elements_2 = main_content_section.find_elements(By.CSS_SELECTOR, "article.my-5 > p")
            
            # Combine content from both selectors
            content_elements = main_content_section
            content = "\n".join([elem.text for elem in content_elements])
            
            news_data['content'] = content
    
        except Exception as e:
            print(f"Error extracting content: {e}")
            news_data['content'] = None

        # Extract author
        try:
            author_element = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div/div[1]/div/section/div[1]/div[1]/ul/li[1]')
            author = author_element.text.strip()

            print(author_element,"===================================")
            # author = author_element.text.strip()  # Remove any leading/trailing whitespace
            news_data['author'] = author
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
            # Locate and extract JSON-LD structured data
            news_data['keywords'] = driver.find_element(By.CSS_SELECTOR, 'meta[name="keywords"]').get_attribute('content').split(',')
        except:
            news_data['keywords'] = []
        news_data['news_subcategory'] = subcategory  # Hardcoding as per your requirement
        news_data['news_type'] = news_type  # Hardcoding as per your requirement
        news_data['media_type'] = 'newspaper'

        # Extract published date and updated date
        try:
            # Locate the element containing both published and updated date information
            date_text = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div/div[1]/div/section/div[1]/div[1]/ul/li[2]').text

            published_date_text = date_text.replace("প্রকাশ : ","")
            
            # Parse the dates to ISO format using helper functions
            published_date = self.parse_bengali_date(published_date_text.strip())
            news_data['published_date'] = published_date.isoformat() if published_date else None
        except Exception as e:
            print(f"Error extracting dates: {e}")
            news_data['published_date'] = None

            # Extract and clean the updated date if available
        try:
            updated_date_text = driver.find_element(By.CSS_SELECTOR, '//*[@id="news1"]/div/div[1]/div/div[1]/div[1]/div[2]/span').text
            updated_date_text = updated_date_text.replace("আপডেট : ","")
            
            # Parse the dates to ISO format using helper functions
            updated_date = self.parse_bengali_date(updated_date_text.strip())
            news_data['updated_date'] = updated_date.isoformat() if updated_date else None
        except Exception as e:
            print(f"Error extracting dates: {e}")
            news_data['updated_date'] = None

        # Add the source and last_scraped time
        news_data['source'] = "দৈনিক নয়া দিগন্ত"
        news_data['last_scraped'] = datetime.now().isoformat()

        # Close the browser when done
        driver.quit()

        return news_data
# scraper = NewsScraper()
# print(scraper.scrape_news_data("https://www.ittefaq.com.bd/687513/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF%E0%A6%B0-%E0%A6%9C%E0%A6%A8%E0%A7%8D%E0%A6%AF-%E0%A6%B8%E0%A7%9F%E0%A6%BE%E0%A6%AC%E0%A6%BF%E0%A6%A8-%E0%A6%A4%E0%A7%87%E0%A6%B2-%E0%A6%93-%E0%A6%AE%E0%A6%B8%E0%A7%81%E0%A6%B0-%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%95%E0%A6%BF%E0%A6%A8%E0%A6%9B%E0%A7%87-%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0"))

# Loading unique links
with open('C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\NayaDigonto\\news_url.json','r', encoding='utf-8') as f:
    d = json.load(f)

all_data = []
for i in d:
    url = i['url']
    type = i['type']
    subcategory = i['subcategory']
    scraper = NewsScraper()
    print(url)
    news_data = scraper.scrape_news_data(url, type, subcategory)
    all_data.append(news_data)

 
try:
    with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\NayaDigonto\\news_data.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = [] 
existing_data.append(all_data)
with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\NayaDigonto\\news_data.json", 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"Saved {len(all_data)} unique links to ittefaq_data.json")
