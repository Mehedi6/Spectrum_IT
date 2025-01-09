import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    visited_urls = []
    start_urls = [

        
        'https://dailyinqilab.com/national',
        'https://dailyinqilab.com/international',
        'https://dailyinqilab.com/islamic-world',
        'https://dailyinqilab.com/politics',
        'https://dailyinqilab.com/economy',
        'https://dailyinqilab.com/sports/cricket',
        'https://dailyinqilab.com/sports/football',
        'https://dailyinqilab.com/sports/others',
        'https://dailyinqilab.com/entertainment/dhallywood',
        'https://dailyinqilab.com/entertainment/bollywood',
        'https://dailyinqilab.com/entertainment/hollywood',
        'https://dailyinqilab.com/entertainment/others',
        'https://dailyinqilab.com/bangladesh',
        'https://dailyinqilab.com/lifestyle',
        'https://dailyinqilab.com/foreign-life',
        'https://dailyinqilab.com/ict-and-career',
        'https://dailyinqilab.com/inter-country',
        'https://dailyinqilab.com/health',
        'https://dailyinqilab.com/literature',
        'https://dailyinqilab.com/motropolis',
        'https://dailyinqilab.com/business',
        
        


    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Inqilab\\news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div.col-md-9.mt-3 > div.row.d-flex.flex-row > a::attr(href), div.col-md-9.mt-3 > div.row.mt-5 > div.col-md-6 > a::attr(href)')
        
        news_type = self.get_news_type(response.url)
        # for news in news_items_1:
        #     yield {
        #         'url': response.urljoin(news.css('::attr(href)').get()),  # Extract the full link
        #         'type': news_type
                
        #     }
        for news in news_items_2:

            if news not in self.visited_urls:
                self.visited_urls.append(news)
                yield {
                    'url': response.urljoin(news.get()),  # Extract the full link
                    'type': news_type[0],
                    'subcategory': news_type[1]
                    
                }
    def get_news_type(self, url):
        if 'national' in url:
            return ['national', 'general']
        elif 'bangladesh' in url or 'inter-country':
            return ['national', 'inter-country']
        elif 'motropolis' in url or 'dhaka' in url:
            return ['national', 'metropolitan']
        
        elif 'politics' in url:
            return ['politics', 'general']
        
        elif 'international' in url:
            return ['international', 'general']
        elif 'islamic-world' in url:
            return ['international', 'islamic-world']
        
        elif 'economy' in url:
            return ['economy', 'general']
        elif 'business' in url:
            return ['economy', 'business']
        
        elif 'entertainment/dhallywood' in url:
            return ['entertainment', 'dhallywood']
        elif 'entertainment/bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'entertainment/hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'entertainment/others' in url:
            return ['entertainment', 'others']
        
        elif 'sports/cricket' in url:
            return ['sports', 'cricket']
        elif 'sports/football' in url:
            return ['sports', 'football']
        elif 'sports/others' in url:
            return ['sports', 'other-sports']
        
        elif 'ict-and-career' in url:
            return ['technology', 'ict-and-career']
        elif 'foreign-life' in url:
            return ['expatriate', 'general']
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        elif 'health' in url:
            return ['health', 'general']
        elif 'literature' in url:
            return ['literature', 'general']
        

        # Check for pagination (if multiple pages)
        # next_page = response.css('a.next::attr(href)').get()  # Adjust based on the next page selector
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()