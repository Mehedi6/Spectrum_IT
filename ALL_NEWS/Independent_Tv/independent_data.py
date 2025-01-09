from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from datetime import datetime
import json
import re
import html
from urllib.parse import urljoin
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewsScraper:
    def bengali_to_english(self, bengali_str):
        # Mapping Bengali numerals to English numerals
        bengali_to_english_digits = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        return bengali_str.translate(bengali_to_english_digits)

    def replace_bengali_strings(self, english_date_str):
        # Replace Bengali month and day names with English equivalents
        month_replacements = {
            'জানুয়ারি': 'January', 'ফেব্রুয়ারি': 'February', 'জানুয়ারি': 'January',
            'জানুয়ারী': 'January', 'জানুয়ারী': 'January', 'ফেব্রুয়ারী': 'February', 
            'মার্চ': 'March','এপ্রিল': 'April', 'মে': 'May', 'জুন': 'June', 'জুলাই': 'July',
            'আগস্ট': 'August', 'সেপ্টেম্বর': 'September', 'অক্টোবর': 'October',
            'নভেম্বর': 'November', 'ডিসেম্বর': 'December'
        }
        day_replacements = {
            'শনিবার': 'Saturday', 'রবিবার': 'Sunday', 'সোমবার': 'Monday',
            'মঙ্গলবার': 'Tuesday', 'বুধবার': 'Wednesday', 'বৃহস্পতিবার': 'Thursday',
            'শুক্রবার': 'Friday'
        }

        for bengali, english in month_replacements.items():
            english_date_str = english_date_str.replace(bengali, english)
        for bengali, english in day_replacements.items():
            english_date_str = english_date_str.replace(bengali, english)
        english_date_str = english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM')
        return english_date_str

    def parse_bengali_date(self, bengali_date_str):
        bengali_date_str = bengali_date_str.replace('প্রকাশ :', '').replace('\xa0', ' ').strip()
        bengali_date_str = bengali_date_str.replace('আপডেট :', '').replace('\xa0', ' ').strip()
        bengali_date_str = self.bengali_to_english(bengali_date_str)
        english_date_str = self.replace_bengali_strings(bengali_date_str)

        print(english_date_str)

        # Fix time format
        english_date_str = re.sub(r'(\d{1,2}):(\d{1,2})', r'\1:\2', english_date_str)
        # print(english_date_str)
        # Parse the date
        try:
            
            return datetime.strptime(english_date_str, "%d %B %Y, %I:%M %p")
        except Exception as e:
            print(f"Error extracting {e}")
            return None

    def scrape_news_data(self, url, news_type, sub_category):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.fullscreen_window()
       
        time.sleep(5)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        news_data = {'url': url, 'news_type': news_type, 'news_subcategory': sub_category}

        news_data['media_type'] = 'Tv Media'
        try:
            # Title
            title = soup.find('meta', property="og:title")
            news_data['title'] = title['content'] if title else None
        except:
            news_data['title'] = None

        
        base_url = "https://www.itvbd.com"  # Replace with the website's base URL
        try:
            # Get all img tags
            
            image = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/span/a/img')
            relative_url = image.get_attribute('src') if image else None
            news_data['image_urls'] = urljoin(base_url, relative_url) if relative_url else None
                
        except Exception as e:
            print(f"Error constructing image URL: {e}")
            news_data['image_urls'] = None
            try:
                # Fallback: Locate video link or other element
                print("Trying to locate the fallback video element...")
                video_element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="ytp-impression-link-content"]'))
                )
                print(video_element,"====")
                video_url = video_element.get_attribute('href')
                news_data['video_urls'] = video_url
            except Exception as fallback_error:
                print(f"Fallback element not found. Error: {fallback_error}")
                news_data['video_urls'] = None
        try:
            # Content
            content_elements = soup.select('#widget_620 > div > div > div > div > div > div > div.row.detail_holder > div > div > div.main_detail_container > div.content_detail_small_width > div > div > div > div > article > div > p')
            news_data['content'] = "\n".join([p.get_text() for p in content_elements]) if content_elements else None
        except:
            news_data['content'] = None

        # Author
        try:
            author = soup.select_one('#widget_620 > div > div > div > div > div > div > div.row.detail_holder > div > div > div.content_detail_small_width1 > div > div > div > div.each_row.author_n_share > div > span')
            news_data['author'] = author.text.strip() if author else None
        except:
            news_data['author'] = None
        
        try:
            # Meta Description
            meta_description = soup.find('meta', property="og:description")
            news_data['meta_description'] = html.unescape(meta_description['content']) if meta_description else None
        except:
            news_data['meta_description'] = None

        # Keywords
        try:
            keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
            keywords = keywords_meta['content'].split(',') if keywords_meta else []
            news_data['keywords'] = list(set(keywords))
        except:
            news_data['keywords'] = []

        # Published Date
        try:
            # Example of simplified CSS selectors targeting key attributes
            published_date_element = soup.select_one('#widget_620 > div > div > div > div > div > div > div.row.detail_holder > div > div > div.content_detail_small_width1 > div > div > div > div.each_row.time > span.tts_time.published_time')
            published_date = published_date_element.text

            index = published_date.find('প্রকাশ :')

            # Extract the substring after 'প্রকাশিত:'
            if index != -1:
                published_date_text = published_date[index+ len('প্রকাশ :'):].strip()
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
            updated_date_element = soup.select_one('#widget_620 > div > div > div > div > div > div > div.row.detail_holder > div > div > div.content_detail_small_width1 > div > div > div > div.each_row.time > span.tts_time.updated_time'
            )
            updated_date = updated_date_element.text
            updated_date = re.sub(r'\s+', ' ', updated_date.replace("আপডেট :", "")).strip()
            index = updated_date.find('আপডেট :')

            # Extract the substring after 'প্রকাশিত:'
            if index != -1:
                updated_date_text = updated_date[index + len('আপডেট :'):].strip()
            else:
                updated_date_text = updated_date

            # Parse the dates to ISO format using helper functions
            updated_date = self.parse_bengali_date(updated_date_text.strip()) 
            news_data['updated_date'] = updated_date.isoformat() if updated_date else None 
        except Exception as e:
            print(f"Error extracting dates {e}")
            news_data['updated_date'] = None

        # Additional Metadata
        news_data['source'] = 'Independent Television'
        news_data['last_scraped'] = datetime.now().isoformat()

        return news_data


# Main Script
try:
    with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Independent_Tv\\independent_data.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

existing_urls = {item['url'] for item in existing_data if item}

with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Independent_Tv\\sample_news_links.json", 'r', encoding='utf-8') as file:
    links_data = json.load(file)

scraper = NewsScraper()
new_data = []
total = 0

for entry in links_data:
    url, news_type, sub_category = entry['url'], entry['news_type'], entry['news_subcategory']
    if url not in existing_urls:
        news_item = scraper.scrape_news_data(url, news_type, sub_category)
        if news_item:
            new_data.append(news_item)
            total += 1

# Save new data
existing_data.extend(new_data)
with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Independent_Tv\\independent_data.json", 'w', encoding='utf-8') as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=4)

print(f"Scraped {total} new articles.")
