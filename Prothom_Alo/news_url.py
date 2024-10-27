import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    visited_urls = []

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }
    start_urls = [
        
        #national
        'https://www.prothomalo.com/bangladesh',
        'https://www.prothomalo.com/bangladesh/capital',
        'https://www.prothomalo.com/bangladesh/district',
        'https://www.prothomalo.com/bangladesh/coronavirus',
        'https://www.prothomalo.com/bangladesh/environment',

        #INTERNATIONAL
        'https://www.prothomalo.com/world',
        # 'https://www.prothomalo.com/collection/palestine-israel-conflict',
        # 'https://www.prothomalo.com/topic/রাশিয়া-ইউক্রেন-সংঘাত',
        # 'https://www.prothomalo.com/world/india',
        # 'https://www.prothomalo.com/world/pakistan',
        # 'https://www.prothomalo.com/world/china',
        # 'https://www.prothomalo.com/world/middle-east',
        # 'https://www.prothomalo.com/world/usa',
        # 'https://www.prothomalo.com/world/asia',
        # 'https://www.prothomalo.com/world/europe',
        # 'https://www.prothomalo.com/world/africa',
        # 'https://www.prothomalo.com/world/south-america',
        
        # #crime
        # 'https://www.prothomalo.com/bangladesh/crime',

        # 'https://www.prothomalo.com/business',
        # 'https://www.prothomalo.com/business/market',
        # 'https://www.prothomalo.com/business/bank',
        # 'https://www.prothomalo.com/business/industry',
        # 'https://www.prothomalo.com/business/economics',
        # 'https://www.prothomalo.com/business/world-business',
        # 'https://www.prothomalo.com/business/analysis',
        # 'https://www.prothomalo.com/business/personal-finance',
        # 'https://www.prothomalo.com/business/উদ্যোক্তা',
        # 'https://www.prothomalo.com/business/corporate',
        # 'https://www.prothomalo.com/collection/budget-2024-25',
    
        # 'https://www.prothomalo.com/opinion',
        # 'https://www.prothomalo.com/opinion/editorial',
        # 'https://www.prothomalo.com/opinion/column',
        # 'https://www.prothomalo.com/opinion/interview',
        # 'https://www.prothomalo.com/opinion/memoir',
        # 'https://www.prothomalo.com/opinion/reaction',
        # 'https://www.prothomalo.com/opinion/letter',
    
        # 'https://www.prothomalo.com/sports',
        # 'https://www.prothomalo.com/sports/cricket',
        # 'https://www.prothomalo.com/sports/football',
        # 'https://www.prothomalo.com/sports/tennis',
        # 'https://www.prothomalo.com/sports/other-sports',
        # 'https://www.prothomalo.com/sports/sports-interview',
        # 'https://www.prothomalo.com/collection/sports-photo-feature',
        # 'https://www.prothomalo.com/collection/sports-quiz',
        # 'https://www.prothomalo.com/collection/bangladesh-southafrica',
    
        # 'https://www.prothomalo.com/entertainment',
        # 'https://www.prothomalo.com/entertainment/tv',
        # 'https://www.prothomalo.com/entertainment/ott',
        # 'https://www.prothomalo.com/entertainment/dhallywood',
        # 'https://www.prothomalo.com/entertainment/tollywood',
        # 'https://www.prothomalo.com/entertainment/bollywood',
        # 'https://www.prothomalo.com/entertainment/hollywood',
        # 'https://www.prothomalo.com/entertainment/world-cinema',
        # 'https://www.prothomalo.com/entertainment/song',
        # 'https://www.prothomalo.com/entertainment/drama',
        # 'https://www.prothomalo.com/entertainment/entertainment-interview',
    
        # 'https://www.prothomalo.com/chakri',
        # 'https://www.prothomalo.com/chakri/chakri-news',
        # 'https://www.prothomalo.com/chakri/employment',
        # 'https://www.prothomalo.com/chakri/chakri-suggestion',
        # 'https://www.prothomalo.com/chakri/chakri-interview',
    
        # 'https://www.prothomalo.com/lifestyle',
        # 'https://www.prothomalo.com/lifestyle/relation',
        # 'https://www.prothomalo.com/lifestyle/horoscope',
        # 'https://www.prothomalo.com/lifestyle/fashion',
        # 'https://www.prothomalo.com/lifestyle/style',
        # 'https://www.prothomalo.com/lifestyle/beauty',
        # 'https://www.prothomalo.com/lifestyle/interior',
        # 'https://www.prothomalo.com/lifestyle/recipe',
        # 'https://www.prothomalo.com/lifestyle/shopping',

        # 'https://www.prothomalo.com/technology',
        # 'https://www.prothomalo.com/technology/gadget',
        # 'https://www.prothomalo.com/technology/advice',
        # 'https://www.prothomalo.com/technology/automobiles',
        # 'https://www.prothomalo.com/technology/cyberworld',
        # 'https://www.prothomalo.com/technology/freelancing',
        # 'https://www.prothomalo.com/technology/artificial-intelligence',

        # 'https://www.prothomalo.com/technology/science',

        # 'https://www.prothomalo.com/education',
        # 'https://www.prothomalo.com/education/admission',
        # 'https://www.prothomalo.com/education/examination',
        # 'https://www.prothomalo.com/education/scholarship',
        # 'https://www.prothomalo.com/education/study',
        # 'https://www.prothomalo.com/education/higher-education',
        # 'https://www.prothomalo.com/education/campus',

        # 'https://www.prothomalo.com/onnoalo',
        # 'https://www.prothomalo.com/onnoalo/poem',
        # 'https://www.prothomalo.com/onnoalo/stories',
        # 'https://www.prothomalo.com/onnoalo/treatise',
        # 'https://www.prothomalo.com/onnoalo/books',
        # 'https://www.prothomalo.com/onnoalo/arts',
        # 'https://www.prothomalo.com/onnoalo/interview',
        # 'https://www.prothomalo.com/onnoalo/travel',
        # 'https://www.prothomalo.com/onnoalo/others',
        # 'https://www.prothomalo.com/onnoalo/translation',
        # 'https://www.prothomalo.com/onnoalo/prose',
        # 'https://www.prothomalo.com/onnoalo/children',

        # 'https://www.prothomalo.com/lifestyle/health',

        'https://www.prothomalo.com/lifestyle/travel',
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
        news_items = response.css('#container > div > div:nth-child(2) > div > div > div._9nRb0.bottom-space > div > div.Ib8Zz > div.wide-story-card.xkXol.HLT9m > div > div.story-data.KlAp7 > div > div > h3 > a')  # Adjust the selector based on the HTML structure
        news_type = self.get_news_type(response.url)
        # sub_news_type = self.get_sub_category(response.url)
        print(news_items,"===========================================================")
        for news in news_items:
            yield {
                'url': response.urljoin(news.css('::attr(href)').get()),  # Extract the full link
                'type': news_type
                
            }
    def get_news_type(self, url):
        if 'bangladesh' in url:
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