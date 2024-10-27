import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):
    name = "link_spider"
    visited_urls = []
    start_urls = [
        # 'https://www.ittefaq.com.bd/national',
        # 'https://www.ittefaq.com.bd/politics',
        # 'https://www.ittefaq.com.bd/world-news',
        # 'https://www.ittefaq.com.bd/sports',
        # 'https://www.ittefaq.com.bd/entertainment',
        # 'https://www.ittefaq.com.bd/business',
        # 'https://www.ittefaq.com.bd/lifestyle',
        # 'https://www.ittefaq.com.bd/tech',
        # 'https://www.ittefaq.com.bd/opinion',
        # 'https://www.ittefaq.com.bd/law-and-court',
        # 'https://www.ittefaq.com.bd/education',
        # 'https://www.ittefaq.com.bd/jobs',
        # 'https://www.ittefaq.com.bd/probash',
        'https://www.prothomalo.com/business/%E0%A6%89%E0%A6%A6%E0%A7%8D%E0%A6%AF%E0%A7%8B%E0%A6%95%E0%A7%8D%E0%A6%A4%E0%A6%BE',
        'https://www.prothomalo.com/business/%E0%A6%89%E0%A6%A6%E0%A7%8D%E0%A6%AF%E0%A7%8B%E0%A6%95%E0%A7%8D%E0%A6%A4%E0%A6%BE'

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
    
        # print(response.url,'====================================================================')
        if response.url not in self.visited_urls: 
            self.visited_urls += [response.url]
            print(response.url,"=========ONE TIME========================================================")
        
process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()