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
    def get_news_type(self, url):
        if '/international/' in url or 'world' in url or 'বিশ্ব' in url:
            if 'world/middle-east' in url:
                return ['international', 'middle-east']
            elif 'world/europe' in url:
                return ['international', 'europe']
            elif 'world/usa' in url:
                return ['international', 'america']
            elif 'world/uk' in url:
                return ['international', 'united-kingdom']
            else:
                return ['international', 'general']
        if 'bangladesh' in url:
            if 'bangladesh/crime-justice' in url:
                return ['crime', 'crime-justice']
            elif 'bangladesh/politics' in url:
                return ['politics', 'general']
            elif 'bangladesh/accident-fire' in url:
                return ['national', 'accident-fire']
            elif 'bangladesh/election' in url:
                return ['national', 'election']
            elif 'bangladesh/agriculture' in url:
                return ['national', 'agriculture']
            else:
                return ['national', 'general']
        elif 'news/chattogram' in url:
            return ['national', 'chittagong']
            
        elif 'student-politics-others' in url:
            return ['politics', 'student-politics']
        elif '/bangladesh/' in url:
            return ['national', 'general']
        
        elif 'economy' in url:
            if 'economy/bank' in url:
                return ['economics', 'bank']
            elif 'economy/industry/taxes-duties' in url:
                return ['economics', 'taxes-duties']
            elif 'economy/industry/port' in url:
                return ['economics', 'industry-port']
            elif 'economy/industry/investment' in url:
                return ['economics', 'investment']
            elif 'economy/share-market' in url:
                return ['economics', 'stock-market']
            elif 'economy/industry' in url:
                return ['economics', 'industry']
            elif 'economy/daily-commodity-price' in url:
                return ['economics', 'daily-commodity-price']
            else:
                return ['economics', 'general']
        elif 'business' in url:
            if 'business/world-economy' in url:
                return ['economics', 'world-economy']
            elif 'business/budget-2024-25' in url or 'business/budget-2022-23':
                return ['economics', 'budget']
            elif 'business/organization-news' in url:
                return ['economics', 'organization-news']
            else:
                return ['economics', 'business']
        elif 'asia' in url:
            if 'asia/india' in url:
                return ['international', 'india']
            else:
                return ['international', 'asia']
            
        elif 'health' in url:
            if 'health/health-care' in url:
                return ['health', 'health-care']
            elif 'health/disease' in url:
                return ['health', 'disease']
            elif 'health/coronavirus' in url:
                return ['health', 'coronavirus']
            else:
                return ['health', 'general']
        
        elif 'sports' in url:
            if 'sports/misc' in url:
                return ['sports', 'miscellaneous']
            elif 'sports/cricket' in url:
                return ['sports', 'cricket']
            elif 'sports/football' in url:
                return ['sports', 'football']
            elif 'sports/other-sports' in url:
                return ['sports', 'other-sports']
            else:
                return ['sports', 'general'] 
        elif 'entertainment' in url:
            if 'entertainment/ওটিটি' in url:
                return ['entertainment', 'ott']
            elif 'entertainment/tv-movies' in url:
                return ['entertainment', 'tv-movies']
            elif 'entertainment/stage-music' in url:
                return ['entertainment', 'stage-music']
            elif 'entertainment/music' in url:
                return ['entertainment', 'music']
            elif 'entertainment/others' in url:
                return ['entertainment', 'others']
            else:
                return ['entertainment', 'general']
        elif 'life-living/travel' in url:
            return ['travel', 'general']
        
        elif 'life-living' in url:
            if 'life-living/food-recipe' in url:
                return ['lifestyle', 'food-recipe']
            elif 'life-living/baby-care-baby-growing' in url:
                return ['lifestyle', 'baby-care-baby-growing']
            elif 'life-living/relation-family' in url:
                return ['lifestyle', 'relation-family']
            elif 'life-living/wellness' in url:
                return ['lifestyle', 'wellness']
            elif 'life-living/fashion-beauty' in url:
                return ['lifestyle', 'fashion-beauty']
            else:
                return ['lifestyle', 'general']
        elif 'literature' in url:
            if 'literature/history-tradition' in url:
                return ['literature', 'history-tradition']
            elif 'literature/art' in url:
                return ['literature', 'art']
            elif 'literature/culture' in url:
                return ['literature', 'culture']
            elif 'literature/story-poem' in url:
                return ['literature', 'story-poem']
            elif 'literature/books' in url:
                return ['literature', 'books']
            elif 'literature/interview' in url:
                return ['literature', 'interview']
            else:
                return ['literature', 'general']

        elif 'education' in url:
            if 'education/campus' in url:
                return ['education', 'campus']
            else:
                return ['education', 'general']
        
        elif 'youth/career' in url:
            if 'youth/career/govt-job' in url:
                return ['jobs', 'govt-job']
            else:
                return ['jobs', 'general']

        elif 'youth' in url:
            if 'youth/inspiration' in url or 'youth/triumph-of-youth' in url:
                return ['youth', 'youth-inspiration']
            elif 'youth/initiative' in url:
                return ['youth', 'initiative']
            elif 'youth/education/student-politics-others' in url:
                return ['youth', 'student-politics-others']
            else:
                return ['youth', 'general']
    
        elif 'tech-startup' in url:
            if 'tech-startup/automobile' in url:
                return ['technology', 'automobile']
            elif 'tech-startup/science-tech-gadgets' in url:
                return ['science', 'science-tech-gadgets']
            elif 'tech-startup/startup' in url:
                return ['technology', 'startup']
            else:
                return ['technology', 'general']
        elif 'abroad/migration' in url or 'abroad/immigration' in url:
            return ['expatriate', 'general']
        
        
        else:
            return ['others', 'others']
    
    
    
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
                                           '#node-367486 > div.pb-20.clearfix > p,'
                                           '#node-325446 > div.pb-20.clearfix > p,'
                                           'div.pb-20.clearfix > p')
            news_data['content'] = "\n".join([p.get_text() for p in content_elements]) if content_elements else None
        except Exception as e:
            print(f"Error extracting content {e}")
            news_data['content'] = None

        # Author
        try:
            author = soup.select_one('#inner-wrap > div.off-canvas-content > main > div > div.block-content.content > div.full-width.detailed-page_2023 > div.container.detailed-body-2023.mt-30 > div > div.detailed-content.columns.medium-3.small-12.detailed-leftsidebar > div.panel-pane.pane-news-details-left.no-title.block > div > div > div.byline-wrapper.row.collapse.align-middle.e-mb-32 > div.content.columns.medium-12.small-12 > div.byline.fw-600.text-16.e-mb-4')
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


csv_file_path = "C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ALL_NEWS\\Daily_Star_Bangla\\daily_star_data.csv"

# Load existing URLs from the CSV file for deduplication
existing_urls = set()
try:
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            existing_urls.add(row['url'])  # Collect existing URLs
except FileNotFoundError:
    # If the CSV file doesn't exist, start fresh
    print("CSV file not found. Starting fresh.")

# Main Script
# try:
#     with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ALL_NEWS\\Bangladesh_Tribune\\all_bdtribune_data.json", 'r', encoding='utf-8') as file:
#         existing_data = json.load(file)
# except FileNotFoundError:
#     existing_data = []

# existing_urls = {item['url'] for item in existing_data}

with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ALL_NEWS\\Daily_Star_Bangla\\final_news_links.json", 'r', encoding='utf-8') as file:
    links_data = json.load(file)

scraper = NewsScraper()
new_data = []
total = 0

# start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)  # Adjust timezone as needed
# end_date = datetime(2024, 12, 31, tzinfo=timezone.utc)

start_date = datetime(2024, 1, 1)  # Adjust timezone as needed
end_date = datetime(2024, 12, 31)
n = int(input("Select no of news to be scrapped: "))
news_count = 0

for entry in links_data:
    try:
        if news_count ==n:
            break
        url = entry['url']
        url = urllib.parse.unquote(url)
        news_type, sub_category = scraper.get_news_type(url)
        if url not in existing_urls:

            news_item = scraper.scrape_news_data(url, news_type, sub_category)
            print(news_item)
            if news_item:
                new_data.append(news_item)
                total += 1
                news_count += 1
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
# existing_data.extend(new_data)

# with open("C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\ALL_NEWS\\Bangladesh_Tribune\\all_bdtribune_data.json", 'w', encoding='utf-8') as file:
#     json.dump(existing_data, file, ensure_ascii=False, indent=4)

# Save the combined data to a CSV file
csv_headers = [
    "url",              # URL of the news article
    "news_type",        # Type of the news (e.g., crime, health, etc.)
    "news_subcategory", # Subcategory of the news (e.g., general)
    "media_type",       # Type of media (e.g., Online News Portal)
    "title",            # Title of the news article
    "image_urls",       # URLs of associated images
    "content",          # Main content of the article
    "author",           # Author of the news article
    "meta_description", # Meta description of the news article
    "keywords",         # Associated keywords (list or comma-separated string)
    "published_date",   # Date when the news was published
    "updated_date",     # Date when the news was last updated
    "source",           # Source of the news
    "last_scraped"      # Date and time when the data was last scraped
]

# Open the CSV file in append mode if it already exists, or write headers if creating a new file
with open(csv_file_path, 'a', encoding='utf-8', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    if csv_file.tell() == 0:  # Write headers only if the file is empty
        writer.writeheader()
    writer.writerows(new_data)  # Append new rows
print(f"Scraped {total} new articles and saved to CSV.")

print(f"Scraped {total} new articles.")
