import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    visited_urls = []
    start_urls = [

        #national
        'https://www.protidinersangbad.com/national',
        'https://www.protidinersangbad.com/whole-country/dhaka',
        'https://www.protidinersangbad.com/whole-country/chittagong',
        'https://www.protidinersangbad.com/whole-country/rajshahi',
        'https://www.protidinersangbad.com/whole-country/khulna',
        'https://www.protidinersangbad.com/whole-country/barisal',
        'https://www.protidinersangbad.com/whole-country/sylhet',
        'https://www.protidinersangbad.com/whole-country/rangpur',
        'https://www.protidinersangbad.com/whole-country/mymensingh',
        'https://www.protidinersangbad.com/justice',
        'https://www.protidinersangbad.com/environment',

        #politics
        'https://www.protidinersangbad.com/politics',
        # #international
        'https://www.protidinersangbad.com/international',

        # #sports
        'https://www.protidinersangbad.com/sports',

        # #entertainment
        'https://www.protidinersangbad.com/entertainment',

        # #education
        'https://www.protidinersangbad.com/education-premises',
        # #economics
        'https://www.protidinersangbad.com/trade',
        'https://www.protidinersangbad.com/trade/share-market',
        # #health
        'https://www.protidinersangbad.com/life-style/health',
        
        # #expatriate
        'https://www.protidinersangbad.com/face-in-abroad',
        # #crime
        'https://www.protidinersangbad.com/crime',

        # #lifestyle
        'https://www.protidinersangbad.com/life-style',
        'https://www.protidinersangbad.com/life-style/fashion-',
        


        # #technology
        'https://www.protidinersangbad.com/science-technology',
   
        # #science
        # 'https://www.kalbela.com/technology/science',
        # #literature
        'https://www.protidinersangbad.com/art-literature',
    
        # #jobs
        'https://www.protidinersangbad.com/jobs',


        
        


    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Protidiner_shongbad\\news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div.col-md-4 > div.content_list > a::attr(href), div.col-lg-12.col > a::attr(href), div.col-lg-8.col > div.position-relative > a::attr(href)')
        
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
        elif 'whole-country/dhaka' in url:
            return ['national', 'capital-city']
        elif 'whole-country/chittagong' in url:
            return ['national', 'chittagong']
        elif 'whole-country/rajshahi' in url:
            return ['national', 'rajshahi']
        elif 'whole-country/khulna' in url:
            return ['national', 'khulna']
        elif 'whole-country/barisal' in url:
            return ['national', 'barisal']
        elif 'whole-country/sylhet' in url:
            return ['national', 'sylhet']
        elif 'whole-country/rangpur' in url:
            return ['national', 'rangpur']
        elif 'whole-country/mymensingh' in url:
            return ['national', 'mymensingh']
        elif 'justice' in url:
            return ['national', 'justice']
        elif 'environment' in url:
            return ['national', 'environment-climate']
        
        elif 'politics' in url:
            return ['politics', 'general']
        
        elif 'international' in url:
            return ['international', 'general']
        
        
        elif 'sports' in url:
            return ['sports', 'general']
        elif 'entertainment' in url:
            return ['entertainment', 'general']
        elif 'education-premises' in url:
            return ['education', 'education-premises']
        elif 'trade/share-market' in url:
            return ['economics', 'share-market']
        elif 'trade' in url:
            return ['economics', 'trade']
        elif 'life-style/health' in url:
            return ['health', 'general']
        elif 'face-in-abroad' in url:
            return ['expatriate', 'general']
        elif 'crime' in url:
            return ['crime', 'general']
        elif 'life-style/fashion' in url:
            return ['lifestyle', 'fashion']
        elif 'life-style' in url:
            return ['lifestyle', 'general']
        elif 'science-technology' in url:
            return ['technology', 'science-technology']
        elif 'art-literature' in url:
            return ['literature', 'general']
        elif 'jobs' in url:
            return ['jobs', 'general']
        
        else:
            return ['others', 'general']
                
        # Check for pagination (if multiple pages)
        # next_page = response.css('a.next::attr(href)').get()  # Adjust based on the next page selector
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()