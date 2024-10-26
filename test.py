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
    # custom_settings = {
    #     'FEED_FORMAT': 'json',
    #     'FEED_URI': 'ittefaq_news_url.json',
    #     'FEED_EXPORT_INDENT': 4,
    #     'LOG_LEVEL': 'DEBUG',
    #     'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
    #     'FEED_EXPORT_ENCODING': 'utf-8',
    #     'DEFAULT': str,
        
    # }


    def parse(self, response):
        # Extract all news articles on the page 
        news_items = response.css('div.info.has_ai > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        print(response.url,"======================")
        
process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()