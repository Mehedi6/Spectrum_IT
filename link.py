import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = [
        'https://www.ittefaq.com.bd/national',
        'https://www.ittefaq.com.bd/politics',
        'https://www.ittefaq.com.bd/world-news',
        'https://www.ittefaq.com.bd/sports',
        'https://www.ittefaq.com.bd/entertainment',
        'https://www.ittefaq.com.bd/business',
        'https://www.ittefaq.com.bd/lifestyle',
        'https://www.ittefaq.com.bd/tech',
        'https://www.ittefaq.com.bd/opinion',
        'https://www.ittefaq.com.bd/law-and-court',
        'https://www.ittefaq.com.bd/education',
        'https://www.ittefaq.com.bd/jobs',
        'https://www.ittefaq.com.bd/probash',
        'https://www.ittefaq.com.bd/literature',

    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'ittefaq_news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        news_items = response.css('div.info.has_ai > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_type = self.get_news_type(response.url)
        for news in news_items:
            yield {
                'url': response.urljoin(news.css('::attr(href)').get()),  # Extract the full link
                'type': news_type
            }
    def get_news_type(self, url):
        if 'national' in url:
            return 'national'
        
        elif 'politics' in url:
            return 'politics'
        
        elif 'world-news' in url:
            return 'international'
        
        elif 'sports' in url:
            return 'sports'
        elif 'entertainment' in url:
            return 'entertainment'
        
        elif 'business' in url:
            return 'business'
        
        elif 'lifestyle' in url:
            return 'lifestyle'
        elif 'tech' in url:
            return 'tech'
        elif 'opinion' in url:
            return 'opinion'
        elif 'law-and-court' in url:
            return 'law-and-court'
        elif 'education' in url:
            return 'education'
        elif 'jobs' in url:
            return 'jobs'
        elif 'probash' in url:
            return 'probash'
        elif 'literature' in url:
            return 'literature'
        else:
            return 'general'

        # Check for pagination (if multiple pages)
        # next_page = response.css('a.next::attr(href)').get()  # Adjust based on the next page selector
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()