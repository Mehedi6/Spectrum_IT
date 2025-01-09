from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from datetime import datetime
import json
import re
import html
from lxml import etree
from urllib.parse import urljoin

class NewsScraper:
    def bengali_to_english(self, bengali_str):
        # Mapping Bengali numerals to English numerals
        bengali_to_english_digits = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        return bengali_str.translate(bengali_to_english_digits)

    def replace_bengali_strings(self, english_date_str):
        # Replace Bengali month and day names with English equivalents
        month_replacements = {
            'জানুয়ারি': 'January', 'ফেব্রুয়ারি': 'February', 'জানুয়ারি': 'January',
            'জানুয়ারী': 'January', 'ফেব্রুয়ারী': 'February', 'মার্চ': 'March',
            'এপ্রিল': 'April', 'মে': 'May', 'জুন': 'June', 'জুলাই': 'July',
            'আগস্ট': 'August', 'সেপ্টেম্বর': 'September', 'অক্টোবর': 'October',
            'নভেম্বর': 'November', 'ডিসেম্বর': 'December', 'ফেব্রুয়ারি': 'February',
            'জানুয়ারী': 'January', 'জানুয়ারী': 'January', 'জানুয়ারি': 'January',
        }
        day_replacements = {
            'শনিবার': 'Saturday', 'রবিবার': 'Sunday', 'সোমবার': 'Monday',
            'মঙ্গলবার': 'Tuesday', 'বুধবার': 'Wednesday', 'বৃহস্পতিবার': 'Thursday',
            'শুক্রবার': 'Friday', 'রোববার': 'Sunday',
        }

        for bengali, english in month_replacements.items():
            english_date_str = english_date_str.replace(bengali, english)
        for bengali, english in day_replacements.items():
            english_date_str = english_date_str.replace(bengali, english)
        english_date_str = english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM').replace('অপরাহ্ন', 'PM').replace('পূর্বাহ্ন', 'AM')
        return english_date_str

    def parse_bengali_date(self, bengali_date_str):
        bengali_date_str = bengali_date_str.replace('প্রকাশ:', '').replace('\xa0', ' ').strip()
        bengali_date_str = bengali_date_str.replace('আপডেট:', '').replace('\xa0', ' ').strip()
        bengali_date_str = self.bengali_to_english(bengali_date_str)
        english_date_str = self.replace_bengali_strings(bengali_date_str)

        print(english_date_str)

        # Fix time format
        english_date_str = re.sub(r'(\d{1,2}):(\d{1,2})', r'\1:\2', english_date_str)
        # print(english_date_str)
        # Parse the date
        try:
            
            return datetime.strptime(english_date_str, "%A %B %d, %Y %I:%M %p")
        except Exception as e:
            print(f"Error extracting {e}")
            return None

    def scrape_news_data(self, url, news_type, sub_category):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return None

        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_data = {'url': url, 'news_type': news_type, 'news_subcategory': sub_category}

        news_data['media_type'] = 'Newspaper'
        try:
            # Title
            title = soup.find('meta', property="og:title")
            news_data['title'] = title['content'] if title else None
        except:
            news_data['title'] = None

        
        base_url = "https://bangla.thedailystar.net"  # Replace with the website's base URL
        try:
            # Get all img tags
            images = soup.select_one('span > picture > img')
            print(f"Found {len(images)} images.")
            image = images
            print(images)

            relative_url = image.get('data-src') or image.get('src') if image else None
            news_data['image_urls'] = urljoin(base_url, relative_url) if relative_url else None
        except Exception as e:
            print(f"Error constructing image URL: {e}")
            news_data['image_urls'] = None

        try:
            # Content
            content_elements = soup.select('div > p.rtejustify,'
                                           '#node-367486 > div.pb-20.clearfix > p')
            news_data['content'] = "\n".join([p.get_text() for p in content_elements]) if content_elements else None
        except:
            news_data['content'] = None

        # Author
        try:
            author = soup.select_one('#inner-wrap > div.off-canvas-content > main > div > div.block-content.content > div.full-width.detailed-page_2023 > div.container.detailed-body-2023.mt-30 > div > div.detailed-content.columns.medium-3.small-12.detailed-leftsidebar > div.panel-pane.pane-news-details-left.no-title.block > div > div > div.byline-wrapper.row.collapse.align-middle.e-mb-32 > div.content.columns.medium-12.small-12 > div.byline.fw-600.text-16.e-mb-4')
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
            published_date_element = soup.select_one('#inner-wrap > div.off-canvas-content > main > div > div.block-content.content > div.full-width.detailed-page_2023 > div.container.detailed-body-2023.mt-30 > div > div.detailed-content.columns.medium-3.small-12.detailed-leftsidebar > div.panel-pane.pane-news-details-left.no-title.block > div > div > div.byline-wrapper.row.collapse.align-middle.e-mb-32 > div.content.columns.medium-12.small-12 > div.date.text-14.lh-20.color-iron')
            published_date = published_date_element.text

            index = published_date.find('সর্বশেষ আপডেট: ')

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
            updated_date_element = soup.select_one('#inner-wrap > div.off-canvas-content > main > div > div.block-content.content > div.full-width.detailed-page_2023 > div.container.detailed-body-2023.mt-30 > div > div.detailed-content.columns.medium-3.small-12.detailed-leftsidebar > div.panel-pane.pane-news-details-left.no-title.block > div > div > div.byline-wrapper.row.collapse.align-middle.e-mb-32 > div.content.columns.medium-12.small-12 > div.date.text-14.lh-20.color-iron'
            )
            updated_date = updated_date_element.text
            index = updated_date.find('সর্বশেষ আপডেট:')

            # Extract the substring after 'সর্বশেষ আপডেট:'
            if index != -1:
                updated_date_text = updated_date[index + len('সর্বশেষ আপডেট:'):].strip()
            else:
                updated_date_text = updated_date

            print(updated_date_text)

            # Parse the dates to ISO format using helper functions
            updated_date = self.parse_bengali_date(updated_date_text.strip()) 
            news_data['updated_date'] = updated_date.isoformat() if updated_date else None 
        except Exception as e:
            print(f"Error extracting dates {e}")
            news_data['updated_date'] = None

        # Additional Metadata
        news_data['source'] = 'The Daily Star Bangla'
        news_data['last_scraped'] = datetime.now().isoformat()

        return news_data


# Main Script
try:
    with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Daily_Star_Bangla\\daily_star_bangla.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

existing_urls = {item['url'] for item in existing_data}

with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Daily_Star_Bangla\\news_links.json", 'r', encoding='utf-8') as file:
    links_data = json.load(file)

scraper = NewsScraper()
new_data = []
total = 0

# start_date = datetime(2024, 1, 1)
# end_date = datetime(2024, 12, 31)

for entry in links_data:
    url, news_type, sub_category = entry['url'], entry['news_type'], entry['news_subcategory']
    if url not in existing_urls:
        news_item = scraper.scrape_news_data(url, news_type, sub_category)
        if news_item:  # Ensure published_date exists
            # Convert ISO string to datetime object
            new_data.append(news_item)
            total += 1
            
            

# Save new data
existing_data.extend(new_data)
with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DRUGS\\Daily_Star_Bangla\\daily_star_bangla.json", 'w', encoding='utf-8') as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=4)

print(f"Scraped {total} new articles.")
