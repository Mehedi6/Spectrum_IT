import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import pytz
import json

class SeoSpider(scrapy.Spider):
    name = "seo_spider"

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Kalerkantho\\news_data.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
    }

    def __init__(self, json_file_path, *args, **kwargs):
        super(SeoSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.load_urls_from_json(json_file_path)
        self.visited_urls = set()

    def load_urls_from_json(self, json_file_path):
        """Loads URLs from a JSON file and returns a list of URLs."""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            urls = [entry["url"] for entry in data if "url" in entry]
            return urls

    def parse(self, response):
        # Iterate over each anchor tag with an href attribute
        for href in response.css('a::attr(href)').extract():
            url = response.urljoin(href)
            # Avoid revisiting already scraped URLs
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        page_data = {
            'url': response.url,
            'title': response.css('title::text').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get(),
            'published_date': self.extract_date(response),
            'updated_date': None,
            'news_type': self.get_news_type(response.url),
            'news_subcategory': response.meta.get('subcategory', 'general'),
            'media_type': 'newspaper',
            'image_urls': (self.extract_image_urls(response))[0] if self.extract_image_urls(response) else None,
            'keywords': self.extract_keywords(response),
            'last_scraped': datetime.now(pytz.timezone('Asia/Dhaka')).isoformat(),
            'source': "যুগান্তর",
            'international': True if self.get_news_type(response.url) == "international" else False,
            'old': False,
            'sentiment': 'neutral',
            'views': 0,
            'news_score': 0,
            'rating': 0,
            'engagement': 0,
            'author': self.extract_author(response),
            'content': self.extract_content(response),
        }
        self.log(f"Extracted data: {page_data}")
        yield page_data

    # Conversion helper methods for Bengali date formats
    def bengali_to_english(self, bengali_str):
        bengali_to_english_digits = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        return bengali_str.translate(bengali_to_english_digits)

    def replace_bengali_strings(self, english_date_str):
        month_replacements = {
            'জানুয়ারি': 'January', 'ফেব্রুয়ারি': 'February', 'মার্চ': 'March',
            'এপ্রিল': 'April', 'মে': 'May', 'জুন': 'June', 'জুলাই': 'July',
            'আগস্ট': 'August', 'সেপ্টেম্বর': 'September', 'অক্টোবর': 'October',
            'নভেম্বর': 'November', 'ডিসেম্বর': 'December'
        }
        for bengali_month, english_month in month_replacements.items():
            english_date_str = english_date_str.replace(bengali_month, english_month)
        return english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM')

    def parse_bengali_date(self, bengali_date_str):
        bengali_date_str = bengali_date_str.replace('প্রকাশ: ', '').strip()
        english_date_str = self.bengali_to_english(bengali_date_str)
        english_date_str = self.replace_bengali_strings(english_date_str)
        try:
            return datetime.strptime(english_date_str, "%d %B %Y, %I:%M %p")
        except ValueError as e:
            self.log(f"Error parsing date: {e}")
            return None

    def extract_date(self, response):
        date_xpath = "//p[@class='desktopDetailPTime color1']/text()"
        date_text = response.xpath(date_xpath).get()
        if date_text:
            return self.parse_bengali_date(date_text)
        return None

    def extract_author(self, response):
        author_tag = response.xpath("div.col-sm-12.col-md-12.col-lg-3.col-xl-2.desktopView > div > h6::text").get()
        return author_tag.strip() if author_tag else None

    def extract_content(self, response):
        content_div = response.css("div.desktopDetailBody p::text").extract()
        return '\n'.join([p.strip() for p in content_div]) if content_div else None

    def extract_image_urls(self, response):
        image_xpath = "//div[contains(@class, 'desktopDetailPhotoDiv')]//figure//img/@src"
        image_urls = response.xpath(image_xpath).extract()
        return [response.urljoin(img_url) for img_url in image_urls]

    def extract_keywords(self, response):
        keywords = response.css('meta[name="keywords"]::attr(content)').get()
        return [kw.strip() for kw in keywords.split(',')] if keywords else None

    def get_news_type(self, url):
        # Placeholder, replace with logic based on the URL structure
        return "general"

# Run the Spider
json_file_path = 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Kalerkantho\\sample_news_links.json'
process = CrawlerProcess()
process.crawl(SeoSpider, json_file_path=json_file_path)
process.start()
