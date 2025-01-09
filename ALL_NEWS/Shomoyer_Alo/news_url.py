import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    visited_urls = []
    start_urls = [

        
        'https://www.shomoyeralo.com/menu/102', #national
        'https://www.shomoyeralo.com/menu/115', #pol
        'https://www.shomoyeralo.com/menu/334', #capital
        'https://www.shomoyeralo.com/menu/107', #whole-country
        'https://www.shomoyeralo.com/menu/116', #intl
        'https://www.shomoyeralo.com/menu/117', #entertain
        'https://www.shomoyeralo.com/menu/329', #football
        'https://www.shomoyeralo.com/menu/330', #cricket
        'https://www.shomoyeralo.com/menu/331', #other-sports
        'https://www.shomoyeralo.com/menu/130', #economy
        'https://www.shomoyeralo.com/menu/123', #education
        'https://www.shomoyeralo.com/menu/332', #campus
        'https://www.shomoyeralo.com/menu/120', #it
        'https://www.shomoyeralo.com/menu/122', #law-justice
        'https://www.shomoyeralo.com/menu/118', #expatriate
        'https://www.shomoyeralo.com/menu/121', #crime
        'https://www.shomoyeralo.com/menu/323', #literature
        'https://www.shomoyeralo.com/menu/141', #lifestyle

        'https://www.shomoyeralo.com/menu/108', #dhaka
        'https://www.shomoyeralo.com/menu/109', #ctg
        'https://www.shomoyeralo.com/menu/110', #raj
        'https://www.shomoyeralo.com/menu/113', #khulna
        'https://www.shomoyeralo.com/menu/112', #sylhet
        'https://www.shomoyeralo.com/menu/111', #barisal
        'https://www.shomoyeralo.com/menu/139', #rangpur
        'https://www.shomoyeralo.com/menu/114', #mymensingh        
        


    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Shomoyer_Alo\\news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div.title_cat > a::attr(href)')
        
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
        if 'menu/102' in url:
            return ['national', 'general']
        elif 'menu/334' in url or 'menu/108' in url:
            return ['national', 'capital-city']
        elif 'menu/122' in url:
            return ['national', 'law-justice']
        
        elif 'menu/107' in url:
            return ['national', 'whole-country']

        elif 'menu/109' in url:
            return ['national', 'chittagong']
        elif 'menu/110' in url:
            return ['national', 'rajshahi']
        elif 'menu/113' in url:
            return ['national', 'khulna']
        elif 'menu/112' in url:
            return ['national', 'sylhet']
        elif 'menu/111' in url:
            return ['national', 'barisal']
        elif 'menu/139' in url:
            return ['national', 'rangpur']
        elif 'menu/114' in url:
            return ['national', 'mymensingh']
        
        elif 'menu/115' in url:
            return ['politics', 'general']
        
        elif 'menu/116' in url:
            return ['international', 'general']
        
        elif 'menu/117' in url:
            return ['entertainment', 'general']
        
        elif 'menu/330' in url:
            return ['sports', 'cricket']
        elif 'menu/329' in url:
            return ['sports', 'football']
        elif 'menu/331' in url:
            return ['sports', 'other-sports']
        
        elif 'menu/130' in url:
            return ['economy', 'general']

        elif 'menu/123' in url:
            return ['education', 'general']
        elif 'menu/332' in url:
            return ['education', 'campus']

        elif 'menu/120' in url:
            return ['technology', 'schience-technology']

        elif 'menu/121' in url:
            return ['crime', 'general']       
        
        
        elif 'menu/118' in url:
            return ['expatriate', 'general']
        elif 'menu/141' in url:
            return ['lifestyle', 'general']
        
        elif 'menu/323' in url:
            return ['literature', 'general']
        

        # Check for pagination (if multiple pages)
        # next_page = response.css('a.next::attr(href)').get()  # Adjust based on the next page selector
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()