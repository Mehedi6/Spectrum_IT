import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    start_urls = [

        #DHAKA_TRIBUNE
        'https://bangla.dhakatribune.com/bangladesh',
        'https://bangla.dhakatribune.com/politics',
        'https://bangla.dhakatribune.com/international',
        'https://bangla.dhakatribune.com/economy',
        'https://bangla.dhakatribune.com/opinion',
        'https://bangla.dhakatribune.com/sport',
        'https://bangla.dhakatribune.com/entertainment',
        'https://bangla.dhakatribune.com/technology',
        'https://bangla.dhakatribune.com/others',


    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\DHAKA_TRIBUNE\\dt_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div > div.info > div > div > div > h2 > a')
        
        news_type = self.get_news_type(response.url)
        # for news in news_items_1:
        #     yield {
        #         'url': response.urljoin(news.css('::attr(href)').get()),  # Extract the full link
        #         'type': news_type
                
        #     }
        for news in news_items_2:
            yield {
                'url': response.urljoin(news.css('::attr(href)').get()),  # Extract the full link
                'type': news_type
                
            }
    def get_news_type(self, url):
        if 'bangladesh' in url:
            return 'national'
        
        elif 'politics' in url:
            return 'politics'
        
        elif 'international' in url:
            return 'international'
        
        elif 'sport' in url:
            return 'sports'
        
        elif 'entertainment' in url:
            return 'entertainment'
        
        elif 'economy' in url:
            return 'business'
        
        elif 'lifestyle' in url:
            return 'lifestyle'
        
        elif 'technology' in url:
            return 'technology'
        
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