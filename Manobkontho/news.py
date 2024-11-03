import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import pytz # type: ignore

class SeoSpider(scrapy.Spider):
    name = "seo_spider"

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Manobkontho\\news.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
    }

    def __init__(self, news_types=None, *args, **kwargs):
        super(SeoSpider, self).__init__(*args, **kwargs)
        self.news_types = news_types if news_types else []
        self.start_urls = self.get_start_urls()
        self.visited_urls = set()
    
    def get_start_urls(self):
        urls=['https://www.manobkantha.com.bd/articlelist/4/national', 
              'https://www.manobkantha.com.bd/articlelist/6/politics',]
       
        return urls

    def parse(self, response):
        

        for href in response.css('div.col-9.col-md-8 > div > h3 > a::attr(href), div.col-12.col-md-8 > div > h2 > a::attr(href), div.col-12.col-md-7 > div > h3 > a::attr(href)').extract():
            url = response.urljoin(href)
           
            if 'national' in url and url not in self.visited_urls:
                yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'general'}) 

                
               
    def parse_page(self, response):
        page_data = {
            'url': response.url,
            'title': response.css('#content > div > div.row.mt-1.mt-sm-3 > div.col-md-9.post-container > div.post > div.post-title > h1::text').get(),
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
            'international': True if self.get_news_type(response.url)=="international" else False,
            'old': False,
            'sentiment': 'neutral',
            'views': 0,
            'news_score': 0,
            'rating': 0,
            'engagement': 0,
            'author': self.extract_author(response),
            'content': self.extract_content(response),
            
        }
        self.log(f"Extracted data: {page_data}")  # Log the extracted data for debugging
        yield page_data

    # Bengali to English date conversion and replacement methods
    def bengali_to_english(self, bengali_str):
        bengali_to_english_digits = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        return bengali_str.translate(bengali_to_english_digits)

    def replace_bengali_strings(self, english_date_str):
        month_replacements = {
            'জানুয়ারি': 'January',
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

        for bengali_month, english_month in month_replacements.items():
            english_date_str = english_date_str.replace(bengali_month, english_month)

        english_date_str = english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM')
        return english_date_str

    def parse_bengali_date(self, bengali_date_str):
        bengali_date_str = bengali_date_str.replace('প্রকাশ: ', '').strip()
        english_date_str = self.bengali_to_english(bengali_date_str)
        english_date_str = self.replace_bengali_strings(english_date_str)

        try:
            return datetime.strptime(english_date_str, "%d %B %Y, %H:%M")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None

    # Extracting date from the page
    def extract_date(self, response):
        # date_xpath = '//*[@id="content"]/div/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/time/text()'
        date_text = response.css('div.post-atribute.d-flex.justify-content-between > div.mt-3.mb-2.text-muted.small.float-start > time::text').get()
        # date_text = response.xpath(date_xpath).get()  # Extract text content directly 
        # print(date_text, "============================")
        
        print(f"Extracted date text: {date_text}")
        if date_text:
            return self.parse_bengali_date(date_text)
        return None

    # Extracting author from the page
    def extract_author(self, response):
        author_tag = response.css("p.desktopDetailReporter::text").get()
        return author_tag.strip() if author_tag else None

    # Extracting content from the page
    def extract_content(self, response):
        content_div = response.css("div.desktopDetailBody p::text").extract()
        content = '\n'.join([p.strip() for p in content_div])
        return content if content else None

    # Extracting image URLs from the page
    def extract_image_urls(self, response):
        image_xpath = "//div[contains(@class, 'desktopDetailPhotoDiv')]//figure//img/@src"
        image_urls = response.xpath(image_xpath).extract()
        return [response.urljoin(img_url) for img_url in image_urls]

    # Extracting keywords from the meta tags
    def extract_keywords(self, response):
        keywords = response.css('meta[name="keywords"]::attr(content)').get()
        return [kw.strip() for kw in keywords.split(',')] if keywords else None

    # Determine the news type from URL
    def get_news_type(self, url):
        if 'asia' in url or 'international' in url or 'europe' in url or 'northamerica' in url or 'southamerica' in url or 'australian-continent' in url or 'malaysia' in url or 'united-states' in url or 'united-kingdom' in url or 'middle-east' in url or 'pakistan' in url or 'india' in url or 'africa' in url or 'international-others' in url:
            return 'international'
        
        if 'economics' in url or 'garments' in url or 'budget' in url or 'share-market' in url or 'tourism' in url or 'revenue' in url or 'import-export' in url or 'bank' in url or 'insurance' in url or 'entrepreneur' in url or 'private-companies' in url or 'economics-others' in url:
            return 'economics'
        
        if ('sports' in url) or ('cricket' in url) or ('football' in url) or ('tenis' in url) or ('sports-interview' in url) or ('sports-others' in url):
            return 'sports'
        
        if ('bnp' in url) or ('awami-league' in url) or ('national-party' in url) or ('jamaat' in url) or ('politics-others' in url):
            return 'politics'
        
        if ('national' in url) or ('government' in url) or ('law-justice' in url) or ('accident' in url) or ('mourning' in url) or ('national-others' in url) or ('media' in url):
            return 'national'
        
        if ('lifestyle' in url) or ('recipe' in url) or ('my-family' in url) or ('travel' in url) or ('solution' in url) or ('cooking' in url) or ('beauty' in url) or ('tips' in url) or ('lifestyle-others' in url) or ('news' in url) or ('legal-advice' in url):
            return 'lifestyle'
       
        if ('travel' in url):
            return 'travel'

        if ('exile' in url):
            return 'expatriate'
        
        if ('entertainment' in url) or ('dhaliwood' in url) or ('bollywood' in url) or ('tollywood' in url) or ('hollywood' in url) or ('entertainment-others' in url) or ('song' in url) or ('drama' in url) or ('entertainment-interview' in url):
            return 'entertainment'

        if ('interview' in url):
            return 'interview'
        
        if ('tech' in url) or ('telco' in url) or ('mobile' in url) or ('it-social-media' in url) or ('apps' in url) or ('invantion' in url) or ('science' in url) or ('freelancing' in url) or ('reviews' in url) or ('tech-others' in url) or ('report' in url) or ('tech-interview' in url):
            return 'tech'
        
        if ('crime' in url):
            return 'crime'
        
        if ('campus' in url) or ('tutorials' in url) or ('admission' in url) or ('exam' in url) or ('results' in url) or ('scholarship' in url) or ('campuses' in url) or ('study-abroad' in url) or ('campus-others' in url):
            return 'education'
        
        if ('job-seek' in url) or ('govt-job' in url) or ('private-job' in url) or ('bank-insurance' in url) or ('state-org' in url) or ('defence' in url) or ('nternational-org' in url) or ('educational-institution' in url) or ('ngo' in url) or ('ecruitment-exam' in url) or ('recruitment-exam-prep' in url) or ('job-seek-media' in url) or ('job-seek-others' in url):
            return 'job'
        
        if ('literature' in url) or ('book-fair' in url) or ('prize' in url) or ('literature-others' in url) or ('prose' in url) or ('poem' in url) or ('literature-interview' in url) or ('book-discussion' in url) or ('news-of-the-art-literature' in url) or ('story' in url):
            return 'literature'
process = CrawlerProcess()
process.crawl(SeoSpider)
process.start()
