from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import urllib.parse
import json
import time, re
import html


class NewsScraper:
    def get_news_category(self, url):
        if 'bangladesh' in url:
            if 'capital' in url:
                return ['national','capital']
            elif 'district' in url:
                return ['national','district']
            elif 'coronavirus' in url:
                return ['national','coronavirus'] 
            elif 'environment' in url:
                return ['national','environment']
            else:
                return ['national', 'general']
        if 'crime' in url:
            return ['crime', 'crime']
        if 'politics' in url:
            return ['politics', 'politics']
        if 'world' in url:
            if 'india' in url:
                return ['international', 'india']
            elif 'pakistan' in url:
                return ['international', 'pakistan'] 
            elif 'china' in url:
                return ['international', 'china']
            elif 'middle-east' in url:
                return ['international', 'middle-east']
            elif 'usa' in url:
                return ['international', 'usa']
            elif 'europe' in url:
                return ['international', 'europe']
            elif 'africa' in url:
                return ['international', 'africa']
            elif 'south-america' in url:
                return ['international', 'south-america']
            else:
                return ['international', 'general']
        if 'business' in url:
            if 'market' in url:
                return ['economics', 'market']
            elif 'bank' in url:
                return ['economics', 'bank']
            elif 'industry' in url:
                return ['economics', 'industry']
            elif 'economics' in url:
                return ['economics', 'economics']
            elif 'world-business' in url:
                return ['economics', 'world-business']
            elif 'analysis' in url:
                return ['economics', 'analysis']
            elif 'personal-finance' in url:
                return ['economics', 'personal-finance']
            elif 'উদ্যোক্তা' in url:
                return ['economics', 'উদ্যোক্তা']
            elif 'corporate' in url:
                return ['economics', 'corporate']
            elif 'budget-2024-25' in url:
                return ['economics', 'budget-2024-25']
            else:
                return ['economics', 'general']
        if 'opinion' in url:
            if 'editorial' in url:
                return ['opinion', 'editorial']
            elif 'column' in url:
                return ['opinion', 'column']
            elif 'interview' in url:
                return ['opinion', 'interview']
            elif 'memoir' in url:
                return ['opinion', 'memoir']
            elif 'reaction' in url:
                return ['opinion', 'reaction']
            elif 'letter' in url:
                return ['opinion','letter']
            else:
                return ['opinion', 'general']
        if 'sports' in url:
            if 'cricket' in url:
                return ['sports', 'cricket']
            elif 'football' in url:
                return ['sports', 'football']
            elif 'tennis' in url:
                return ['sports','tennis']
            elif 'other-sports' in url:
                return ['sports', 'other-sports']
            elif 'sports-interview' in url:
                return ['sports','sports-interview']
            else:
                return ['sports', 'general']
        if 'entertainment' in url:
            if 'tv' in url:
                return ['entertainment', 'tv']
            elif 'ott' in url:
                return ['entertainment', 'ott']
            elif 'dhallywood' in url:
                return ['entertainment', 'dhallywood']
            elif 'tollywood' in url:
                return ['entertainment', 'tollywood']
            elif 'bollywood' in url:
                return ['entertainment', 'bollywood']
            elif 'hollywood' in url:
                return ['entertainment', 'hollywood']
            elif 'world-cinema' in url:
                return ['entertainment', 'world-cinema']
            elif 'song' in url:
                return ['entertainment', 'song']
            elif 'drama' in url:
                return ['entertainment', 'drama']
            elif 'entertainment-interview' in url:
                return ['entertainment', 'entertainment-interview']
            else:
                return ['entertainment', 'general']
        if 'chakri' in url:
            if 'chakri-news' in url:
                return ['job', 'chakri-news']
            elif 'employment' in url:
                return ['job', 'employment']
            elif 'chakri-suggestion' in url:
                return ['job', 'chakri-suggestion']
            elif 'chakri-interview' in url:
                return ['job', 'chakri-interview']
            else:
                return ['job', 'general']
        if 'lifestyle' in url:
            if 'relation' in url:
                return ['lifestyle', 'relation']
            elif 'horoscope' in url:
                return ['lifestyle', 'horoscope']
            elif 'fashion' in url:
                return ['lifestyle', 'fashion']
            elif 'style' in url:
                return ['lifestyle', 'style']
            elif 'beauty' in url:
                return ['lifestyle', 'beauty']
            elif 'interior' in url:
                return ['lifestyle', 'interior']
            elif 'recipe' in url:
                return ['lifestyle', 'recipe']
            elif 'shopping' in url:
                return ['lifestyle', 'shopping']
            else:
                return ['lifestyle', 'general']
        if 'technology' in url:
            if 'gadget' in url:
                return ['technology', 'gadget']
            elif 'advice' in url:
                return ['technology', 'advice']
            elif 'automobiles' in url:
                return ['technology', 'automobiles']
            elif 'cyberworld' in url:
                return ['technology', 'cyberworld']
            elif 'freelancing' in url:
                return ['technology', 'freelancing']
            elif 'artificial-intelligence' in url:
                return ['technology', 'artificial-intelligence']
            else:
                return ['technology', 'general']
        if 'science' in url:
            return ['science', 'science']
        if 'education' in url:
            if 'admission' in url:
                return ['education', 'admission']
            elif 'examination' in url:
                return ['education', 'examination']
            elif 'scholarship' in url:
                return ['education', 'scholarship']
            elif 'study' in url:
                return ['education', 'study']
            elif 'higher-education' in url:
                return ['education', 'higher-education']
            elif 'campus' in url:
                return ['education', 'campus']
            else:
                return ['education', 'general']
        if 'onnoalo' in url:
            if 'poem' in url:
                return ['literature', 'poem']
            elif 'stories' in url:
                return ['literature', 'stories']
            elif 'treatise' in url:
                return ['literature', 'treatise']
            elif 'books' in url:
                return ['literature', 'books']
            elif 'arts' in url:
                return ['literature', 'arts']
            elif 'interview' in url:
                return ['literature', 'interview']
            elif 'others' in url:
                return ['literature', 'others']
            elif 'translation' in url:
                return ['literature', 'translation']
            elif 'prose' in url:
                return ['literature', 'prose']
            elif 'children' in url:
                return ['literature', 'children']
            else:
                return ['literature', 'general']
        if 'travel' in url:
            return ['travel', 'travel']
        
        
            
            
            
            
    
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
        for bengali_month, english_month in month_replacements.items():
            english_date_str = english_date_str.replace(bengali_month, english_month)        
        # Replace Bengali AM/PM with English equivalents
        english_date_str = english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM')        
        return english_date_str

    def parse_bengali_date(self, bengali_date_str):
        # Remove the 'প্রকাশ' part and strip any extra whitespace
        bengali_date_str = bengali_date_str.replace('প্রকাশ: ', '').strip()
        bengali_date_str = bengali_date_str.replace('আপডেট: ', '').strip()
        
        # Convert Bengali numbers to English
        english_date_str = self.bengali_to_english(bengali_date_str)
        
        # Replace Bengali month names with English ones
        english_date_str = self.replace_bengali_strings(english_date_str)
        
        # Handle the case with the extra space in the time part
        english_date_str = re.sub(r'(\d{2}):\s(\d{2})', r'\1:\2', english_date_str)  # Fix extra space in time
        
        print(f"Final date string for parsing: {english_date_str}")  # Debugging print
        
        # Define the format for parsing (using 24-hour format)
        try:
            return datetime.strptime(english_date_str, "%d %B %Y, %H:%M")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None  # or handle error accordingly
        


    def scrape_news_data(self, url):
        # Configure ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(), options=chrome_options)

        # Open the URL
        driver.get(url)
        driver.maximize_window()
        time.sleep(4)
        
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
            image_url = driver.find_elements(By.CSS_SELECTOR, 'div > div > div > div > div > figure > picture > img')
            image_url = image_url[0].get_attribute('src')
            news_data['image_urls'] = image_url
        except Exception as e:
            print(f"Error extracting image URL: {e}")
            news_data['image_urls'] = None

        # Extract content
        try:
            content_element = driver.find_elements(By.CSS_SELECTOR, 'div.story-content.no-key-elements p') 
            content = "\n".join([elem.text for elem in content_element])
            news_data['content'] = content
        except Exception as e:
            print(f"Error extracting content: {e}")
            news_data['content'] = None

        # Extract author
        try:
            author_element = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/div')
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
        keywords = ['TCB', 'টিসিবি', 'ট্রেডিং করপোরেশন অব বাংলাদেশ (টিসিবি)']
       
        try:
            # Look for additional dynamic keywords in the content
            content_keywords = []
            if any(kw in content for kw in ['টিসিবির ফ্যামিলি কার্ড', 'ফ্যামিলি কার্ড']):
                content_keywords.extend(['টিসিবির ফ্যামিলি কার্ড', 'ফ্যামিলি কার্ড'])
            
            if any(kw in content for kw in ['টিসিবির পণ্য বিক্রি', 'টিসিবির পণ্য', 'পণ্য বিক্রি']):
                content_keywords.extend(['টিসিবির পণ্য বিক্রি', 'টিসিবির পণ্য', 'পণ্য বিক্রি'])
            
            keywords.extend(content_keywords)
            
            # Add meta keywords if present
            meta_keywords = driver.find_element(By.CSS_SELECTOR, 'meta[name="keywords"]').get_attribute('content').split(',')
            keywords.extend(meta_keywords)
            # Remove duplicates
            news_data['keywords'] = list(set(keywords))
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            news_data['keywords'] = list(set(keywords))

        # Extract news subcategory and type
        # news_data['keywords'] = driver.find_element(By.CSS_SELECTOR, 'meta[name="keywords"]').get_attribute('content').split(',')
        # category = self.get_news_category(url) 
        # try:
        #     news_data['news_subcategory'] = category[1] # Hardcoding as per your requirement
        #     news_data['news_type'] = category[0]  # Hardcoding as per your requirement
        # except Exception as e:
        #     news_data['news_subcategory'] = None # Hardcoding as per your requirement
        #     news_data['news_type'] = None
        news_data['media_type'] = 'newspaper'
        # News Type and Subcategory (Fixed values)
        news_data['news_type'] = "Economics"
        news_data['news_subcategory'] = "Market"

        # Extract published date and updated date
        try:
            published_date_text = driver.find_element(By.CSS_SELECTOR, 'div.time-social-share-wrapper._24WTx > div.xuoYp > time').text
            if "প্রকাশ:" in published_date_text:
                published_date_text = published_date_text.replace("প্রকাশ: ","")
                
                # Parse the dates to ISO format using helper functions
                published_date = self.parse_bengali_date(published_date_text.strip())
                
                news_data['published_date'] = published_date.isoformat() if published_date else None
                news_data['updated_date'] = None
            else:
                updated_date_text = published_date_text.replace("আপডেট: ","")
            
                # Parse the dates to ISO format using helper functions
                updated_date = self.parse_bengali_date(updated_date_text.strip())
                news_data['updated_date'] = updated_date.isoformat() if updated_date else None

                time.sleep(2)  # You can adjust this time based on your page load speed
                # Find the toggle button (XPath you provided)
                toggle_button_xpath = '//div[@class="xuoYp"]'

                # Click the toggle button to update the date
                # Wait until the element is clickable
                toggle_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, toggle_button_xpath))
                )
                toggle_button.click()

                # Wait for a moment to ensure the page has updated
                
                # Wait for the published date to appear
                published_date_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.time-social-share-wrapper._24WTx > div.xuoYp > time'))
                )
                
                # Clean the text to get the date
                published_date_text = published_date_element.text.replace("প্রকাশ: ", "")
                
                # Parse the dates to ISO format using helper functions
                published_date = self.parse_bengali_date(published_date_text.strip())
                news_data['published_date'] = published_date.isoformat() if published_date else None
        except Exception as e:
            print(f"Error extracting dates: {e}")
            news_data['published_date'] = None
        

        # Add the source and last_scraped time
        news_data['source'] = "দৈনিক প্রথম আলো"
        news_data['last_scraped'] = datetime.now().isoformat()

        # Close the browser when done
        driver.quit()

        return news_data
# scraper = NewsScraper()
# print(scraper.scrape_news_data("https://www.ittefaq.com.bd/687513/%E0%A6%9F%E0%A6%BF%E0%A6%B8%E0%A6%BF%E0%A6%AC%E0%A6%BF%E0%A6%B0-%E0%A6%9C%E0%A6%A8%E0%A7%8D%E0%A6%AF-%E0%A6%B8%E0%A7%9F%E0%A6%BE%E0%A6%AC%E0%A6%BF%E0%A6%A8-%E0%A6%A4%E0%A7%87%E0%A6%B2-%E0%A6%93-%E0%A6%AE%E0%A6%B8%E0%A7%81%E0%A6%B0-%E0%A6%A1%E0%A6%BE%E0%A6%B2-%E0%A6%95%E0%A6%BF%E0%A6%A8%E0%A6%9B%E0%A7%87-%E0%A6%B8%E0%A6%B0%E0%A6%95%E0%A6%BE%E0%A6%B0"))

# Loading unique links
try:
    with open("C:\\Users\\arwen\\Desktop\\TCB\\Prothom_Alo\\prothomalo_data.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []  # Initialize empty if file doesn't exist

# Extract only new URLs not already in the file
existing_url = {item['url'] for item in existing_data}

with open('C:\\Users\\arwen\\Desktop\\TCB\\Prothom_Alo\\prothom_alo_news_links.json') as f:
    d = json.load(f)

all_data = []
for i in d:
    url = i['url']
    if url not in existing_url and 'video' not in url:
        scraper = NewsScraper()
        news_data = scraper.scrape_news_data(url)
        print(news_data)
        all_data.append(news_data)
    else:
        continue
 

# filtered_new_data = [item for item in all_data if item['url'] not in existing_url]

# Append new data to existing data and write back to JSON
existing_data.extend(all_data)
with open("C:\\Users\\arwen\\Desktop\\TCB\\Prothom_Alo\\prothomalo_data.json", 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"Saved {len(all_data)} unique links to prothomalo_data.json")