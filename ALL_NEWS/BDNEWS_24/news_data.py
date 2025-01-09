from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from datetime import datetime, timezone
import json
import csv
import re
import html
import urllib.parse
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
            
            return datetime.strptime(english_date_str, "%d %b %Y, %I:%M %p")
        except Exception as e:
            print(f"Error extracting {e}")
            return None

    def scrape_news_data(self, url, news_type, sub_category):
        try:
            # Attempt to fetch the content of the URL
            response = requests.get(url, timeout=10)  # Add a timeout for better control
        except requests.exceptions.RequestException as e:
            # Catch any request-related errors
            print(f"Failed to fetch {url}: {e}")
            return None  # Return None if the request fails

        # Check if the status code indicates success
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return None  # Return None for non-200 responses

        # Parse the content using BeautifulSoup
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            # Catch any parsing errors
            print(f"Error parsing content from {url}: {e}")
            return None  # Return None if parsing fails
        
        news_data = {'url': url, 'news_type': news_type, 'news_subcategory': sub_category}

        news_data['media_type'] = 'Online News Portal'
        try:
            # Title
            title = soup.find('meta', property="og:title")
            news_data['title'] = title['content'] if title else None
        except Exception as e:
            print(f"Error extracting title {e}")
            news_data['title'] = None

        
        base_url = "https://bangla.bdnews24.com"  # Replace with the website's base URL
        try:
            # Get all img tags
            images = soup.select_one('picture > img')
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
            content_elements = soup.select('#contentDetails > div > div > p')
            news_data['content'] = "\n".join([p.get_text() for p in content_elements]) if content_elements else None
        except Exception as e:
            print(f"Error extracting content {e}")
            news_data['content'] = None

        # Author
        try:
            author = soup.select_one('body > main > section.Deatils-wrapper.mt-4 > div > div > div.col-md-9.Dtop-30.rowresize > div.detail-author-name.print-section.d-flex.align-items-center > div > div > p > span')
            news_data['author'] = author.text.strip() if author else None
        except Exception as e:
            print(f"Error extracting author {e}")
            news_data['author'] = None
        
        try:
            # Meta Description
            meta_description = soup.find('meta', property="og:description")
            news_data['meta_description'] = html.unescape(meta_description['content']) if meta_description else None
        except Exception as e:
            print(f"Error extracting meta-description {e}")
            news_data['meta_description'] = None

        # Keywords
        try:
            keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
            keywords = keywords_meta['content'].split(',') if keywords_meta else []
            news_data['keywords'] = list(set(keywords))
        except Exception as e:
            print(f"Error extracting keywords {e}")
            news_data['keywords'] = []

        # Published Date
        try:
            # Example of simplified CSS selectors targeting key attributes
            published_date_element = soup.select_one('body > main > section.Deatils-wrapper.mt-4 > div > div > div.col-md-9.Dtop-30.rowresize > div.pub-up.print-section.d-lg-flex > p:nth-child(1) > span:nth-child(2)')
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
            updated_date_element = soup.select_one('body > main > section.Deatils-wrapper.mt-4 > div > div > div.col-md-9.Dtop-30.rowresize > div.pub-up.print-section.d-lg-flex > p:nth-child(2) > span'
            )
            updated_date = updated_date_element.text
            index = updated_date.find('Updated :')
            print(updated_date,"=======")
            # Extract the substring after 'সর্বশেষ আপডেট:'
            if index != -1:
                updated_date_text = updated_date[index + len('UPDATED :'):].strip()
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
        news_data['source'] = 'Bdnews24'
        news_data['last_scraped'] = datetime.now().isoformat()

        return news_data


# csv_file_path = "bdnews24_data.csv"

# # Load existing URLs from the CSV file for deduplication
# existing_urls = set()
# try:
#     with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
#         reader = csv.DictReader(csv_file)
#         for row in reader:
#             existing_urls.add(row['url'])  # Collect existing URLs
# except FileNotFoundError:
#     # If the CSV file doesn't exist, start fresh
#     print("CSV file not found. Starting fresh.")

# Main Script
try:
    with open("data.json", 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

existing_urls = {item['url'] for item in existing_data}

with open("news_links.json", 'r', encoding='utf-8') as file:
    links_data = json.load(file)

scraper = NewsScraper()
new_data = []
total = 0

# start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)  # Adjust timezone as needed
# end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)

start_date = datetime(2024, 1, 1)  # Adjust timezone as needed
end_date = datetime(2024, 12, 31)

for entry in links_data:
    try:
        url = entry['url']
        url = urllib.parse.unquote(url)
        
        news_type, sub_category = entry['news_type'], entry['news_subcategory']
        if url not in existing_urls:

            news_item = scraper.scrape_news_data(url, news_type, sub_category)
            print(news_item)
            if news_item:
                new_data.append(news_item)
                total += 1
            # else:
            #     print(f"Date not in 2024")
            #     break
    except Exception as e:
        print(f"Error processing entry {entry}: {e}")
        break
# for entry in links_data:
#     url, news_type, sub_category = entry['url'], entry['news_type'], entry['news_subcategory']
#     if url not in existing_urls:
#         news_item = scraper.scrape_news_data(url, news_type, sub_category)
#         if news_item and news_item.get('published_date'):  # Ensure published_date exists
#             # Convert ISO string to datetime object
#             published_date = datetime.fromisoformat(news_item['published_date'])
            
#             # Check if the date is within the specified range
#             if start_date <= published_date <= end_date:
#                 new_data.append(news_item)
#                 total += 1
#             else:
#                 print(f"Date not in 2024")

# for entry in links_data:
#     try:
#         url, news_type, sub_category, published_date = entry['url'], entry['news_type'], entry['news_subcategory'], entry['published_date']
#         if url in existing_urls:
#             published_date = datetime.fromisoformat(published_date)
#             print(url)
#             for item in existing_data:
#                 if item['url'] == url and (item.get('author') is None or item.get('content') is None):
#                     if start_date <= published_date <= end_date:
#                         news_item = scraper.scrape_news_data(url, news_type, sub_category)
#                         item.update(news_item)
#                         break
#             # Check if the date is within the specified range
#                     else:
#                         print(f"Date not in 2024")
#                         break
#     except Exception as e:
#         print(f"Error processing entry {entry}: {e}")
    
        

# Save new data
existing_data.extend(new_data)

with open("data.json", 'w', encoding='utf-8') as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=4)

# Save the combined data to a CSV file
# csv_headers = [
#     "url",              # URL of the news article
#     "news_type",        # Type of the news (e.g., crime, health, etc.)
#     "news_subcategory", # Subcategory of the news (e.g., general)
#     "media_type",       # Type of media (e.g., Online News Portal)
#     "title",            # Title of the news article
#     "image_urls",       # URLs of associated images
#     "content",          # Main content of the article
#     "author",           # Author of the news article
#     "meta_description", # Meta description of the news article
#     "keywords",         # Associated keywords (list or comma-separated string)
#     "published_date",   # Date when the news was published
#     "updated_date",     # Date when the news was last updated
#     "source",           # Source of the news
#     "last_scraped"      # Date and time when the data was last scraped
# ]

# # Open the CSV file in append mode if it already exists, or write headers if creating a new file
# with open(csv_file_path, 'a', encoding='utf-8', newline='') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
#     if csv_file.tell() == 0:  # Write headers only if the file is empty
#         writer.writeheader()
#     writer.writerows(new_data)  # Append new rows
# print(f"Scraped {total} new articles and saved to CSV.")

# print(f"Scraped {total} new articles.")
