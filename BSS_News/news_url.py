# import scrapy
# from scrapy.crawler import CrawlerProcess

# class LinkSpider(scrapy.Spider):

#     name = "link_spider"
#     visited_urls = []

#     custom_settings = {
#         'FEED_FORMAT': 'json',
#         'FEED_URI': 'C:\\Users\\arwen\Desktop\\Newspaper Scraping\\Spectrum_IT\\BSS_News\\news_url.json',
#         'FEED_EXPORT_INDENT': 4,
#         'LOG_LEVEL': 'DEBUG',
#         'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
#         'FEED_EXPORT_ENCODING': 'utf-8',
#         'DEFAULT': str,
        
#     }
#     start_urls = [
        
#         #national
#         # 'https://www.bssnews.net/bangla/national',
#         # 'https://www.bssnews.net/bangla/national/chief-advisers-news',
#         # 'https://www.bssnews.net/bangla/national/national-news',
#         # # 'https://www.bssnews.net/bangla/national/top-news',
#         # # 'https://www.bssnews.net/bangla/national/president',
#         # # 'https://www.bssnews.net/bangla/national/district-news',
#         # # 'https://www.bssnews.net/bangla/national/agriculture-news',
#         # # 'https://www.bssnews.net/bangla/national/weather',

#         # 'https://www.bssnews.net/bangla/national/education',
#         'https://www.bssnews.net/bangla/international',

#         # 'https://www.bssnews.net/bangla/sports',
#         # 'https://www.bssnews.net/bangla/trade',

#         # 'https://www.bssnews.net/bangla/',

#         ]


#     def parse(self, response):
#         # Extract all news articles on the page 
#         news_items = response.css('body > div.panel-body > div > div > div > div.row > div > div > a')  # Adjust the selector based on the HTML structure
#         news_type = self.get_news_type(response.url)
#         for news in news_items:
#             yield {
#                 'url': response.urljoin(news.css('::attr(href)').get()),  # Extract the full link
#                 'news_type': news_type[0],
#                 'news_subcategory': news_type[1],
                
#             }
#         # Check for pagination (if multiple pages)
#         # next_page = response.css('body > div.panel-body > div > div > div > a::href')  # Adjust based on the next page selector
#         # if next_page:
#         #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
#     def get_news_type(self, url):
#         if 'national/education' in url:
#             return ['education', 'education']
#         elif 'national' in url:
#             if 'chief-advisers-news' in url:
#                 return ['national', 'chief-advisers-news']
#             elif 'national-news' in url:
#                 return ['national', 'national-news']
#             elif 'top-news' in url:
#                 return ['national', 'top-news']
#             elif 'president' in url:
#                 return ['national', 'president']
#             elif 'district-news' in url:
#                 return ['national', 'district-news']
#             elif 'agriculture-news' in url:
#                 return ['national', 'agriculture-news']
#             elif 'weather' in url:
#                 return ['national', 'weather']
#         elif 'international' in url:
#             return ['international', 'international']
        
#         elif 'politics' in url:
#             return 'politics'
        
#         elif 'sports' in url:
#             return ['sports', 'sports']
        
#         elif 'trade' in url:
#             return ['trade', 'trade']
        

        
        
        
        
#         elif 'entertainment' in url:
#             return 'entertainment'
        
#         elif 'business' in url:
#             return 'business'
        
#         elif 'lifestyle' in url:
#             return 'lifestyle'
#         elif 'tech' in url:
#             return 'tech'
#         elif 'opinion' in url:
#             return 'opinion'
#         elif 'law-and-court' in url:
#             return 'law-and-court'
#         elif 'education' in url:
#             return 'education'
#         elif 'jobs' in url:
#             return 'jobs'
#         elif 'probash' in url:
#             return 'probash'
#         elif 'literature' in url:
#             return 'literature'
#         else:
#             return 'general'

    

# process = CrawlerProcess()
# process.crawl(LinkSpider)
# process.start()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time, json

def scrape_links(output_file_name, urls_to_scrape):
    # Configure ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    # wait = WebDriverWait(driver, 5)

    # Scroll down the page
    def scroll_down():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for content to load after scrolling

    def get_news_type(url):
        if 'national/education' in url:
            return ['education', 'education']
        elif 'national' in url:
            if 'chief-advisers-news' in url:
                return ['national', 'chief-advisers-news']
            elif 'national-news' in url:
                return ['national', 'national-news']
            elif 'top-news' in url:
                return ['national', 'top-news']
            elif 'president' in url:
                return ['national', 'president']
            elif 'district-news' in url:
                return ['national', 'district-news']
            elif 'agriculture-news' in url:
                return ['national', 'agriculture-news']
            elif 'weather' in url:
                return ['national', 'weather']
        elif 'international' in url:
            return ['international', 'international']
        
        elif 'politics' in url:
            return 'politics'
        
        elif 'sports' in url:
            return ['sports', 'sports']
        
        elif 'trade' in url:
            return ['trade', 'trade']
    def extract_links():
        links = set()  # Use a set to avoid duplicates
        
        card_elements = driver.find_elements(By.CSS_SELECTOR, 'body > div.panel-body > div > div > div > div.row > div > div > a')

        print(len(card_elements))
        for card in card_elements:
            link = card.get_attribute('href')
            if link:
                links.add(link)
        
        print(links,"==============================")

        return links  # Return the unique links as a set
    
    all_links = set()
    for url in urls_to_scrape:
        print(f"Processing: {url}")
        # Open the website
        driver.get(url)
        # driver.maximize_window()

        # Wait for the page to fully load
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        # # Step 1: Click all "See More" buttons
        # click_see_more_button()

        # Step 2: Extract all the links from the loaded content
        links_data = extract_links()
        news_types = get_news_type(url)
        news_type = news_types[0]
        news_subcategory = news_types[1]
        # all_links.update(links_data)  # Update the set to ensure all links are unique
        for link in links_data:
            all_links.add((link, news_type, news_subcategory))
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

    driver.quit()

    



start_urls = [
        
        #national
        # 'https://www.bssnews.net/bangla/national',
        'https://www.bssnews.net/bangla/national/chief-advisers-news',
        'https://www.bssnews.net/bangla/national/national-news',
        'https://www.bssnews.net/bangla/national/top-news',
        'https://www.bssnews.net/bangla/national/president',
        'https://www.bssnews.net/bangla/national/district-news',
        'https://www.bssnews.net/bangla/national/agriculture-news',
        'https://www.bssnews.net/bangla/national/weather',

        'https://www.bssnews.net/bangla/national/education',
        # 'https://www.bssnews.net/bangla/international',

        'https://www.bssnews.net/bangla/sports',
        'https://www.bssnews.net/bangla/trade',


        ]
scrape_links('C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\BSS_News\\news_urls.json',start_urls)


