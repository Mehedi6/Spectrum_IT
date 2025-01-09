import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    visited_urls = []
    start_urls = [

        #DHAKA_TRIBUNE
        'https://www.manobkantha.com.bd/articlelist/4/national',
        'https://www.manobkantha.com.bd/articlelist/6/politics',
        'https://www.manobkantha.com.bd//articlelist/29/law',
        'https://www.manobkantha.com.bd/articlelist/17/dhaka',
        'https://www.manobkantha.com.bd/articlelist/18/chattogram',
        'https://www.manobkantha.com.bd/articlelist/20/sylhet',
        'https://www.manobkantha.com.bd/articlelist/21/barisal',
        'https://www.manobkantha.com.bd/articlelist/22/khulna',
        'https://www.manobkantha.com.bd/articlelist/23/rangpur',
        'https://www.manobkantha.com.bd/articlelist/24/mymensingh',
        'https://www.manobkantha.com.bd/articlelist/19/rajshahi',
        'https://www.manobkantha.com.bd/articlelist/7/international',
        'https://www.manobkantha.com.bd/articlelist/8/entertainment',
        'https://www.manobkantha.com.bd/articlelist/9/sports',
        'https://www.manobkantha.com.bd/articlelist/10/campus',
        'https://www.manobkantha.com.bd/articlelist/13/it',
        'https://www.manobkantha.com.bd/articlelist/41/job',
        'https://www.manobkantha.com.bd/articlelist/38/lifestyle',
        'https://www.manobkantha.com.bd/articlelist/12/economics',
        'https://www.manobkantha.com.bd/articlelist/25/eco-ministries',
        'https://www.manobkantha.com.bd/articlelist/27/economic-others',
        'https://www.manobkantha.com.bd/articlelist/26/bank-insurance',
        'https://www.manobkantha.com.bd//articlelist/28/literature',
        'https://www.manobkantha.com.bd//articlelist/34/city',
        'https://www.manobkantha.com.bd//articlelist/31/probash',
        'https://www.manobkantha.com.bd//articlelist/42/crime',
        
        


    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Manobkontho\\news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div.col-9.col-md-8 > div > h3 > a::attr(href), div.col-12.col-md-8 > div > h2 > a::attr(href), div.col-12.col-md-7 > div > h3 > a::attr(href)')
        
        news_type = self.get_news_type(response.url)
        # for news in news_items_1:
        #     yield {
        #         'url': response.urljoin(news.css('::attr(href)').get()),  # Extract the full link
        #         'type': news_type
                
        #     }
        for news in news_items_2:
            yield {
                'url': response.urljoin(news.get()),  # Extract the full link
                'type': news_type[0],
                'subcategory': news_type[1]
                
            }
    def get_news_type(self, url):
        if 'national' in url:
            return ['national', 'general']
        elif 'law' in url:
            return ['national', 'law']
        elif 'city' in url or 'dhaka' in url:
            return ['national', 'capital-city']
        elif 'politics' in url:
            return ['politics', 'general']
        elif 'chattogram' in url:
            return ['national', 'chittagong']
        elif 'sylhet' in url:
            return ['national', 'sylhet']
        elif 'barisal' in url:
            return ['national', 'barisal']
        elif 'khulna' in url:
            return ['national', 'khulna']
        elif 'rangpur' in url:
            return ['national', 'rangpur']
        elif 'mymensingh' in url:
            return ['national', 'mymensingh']
        elif 'rajshahi' in url:
            return ['national', 'rajshahi']
        elif 'international' in url:
            return ['international', 'general']
        elif 'entertainment' in url:
            return ['entertainment', 'general']
        elif 'sports' in url:
            return ['sports', 'general']
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'it' in url:
            return ['technology', 'general']
        elif 'job' in url:
            return ['job', 'general']
        elif 'lifestyle' in url:
            return ['lifestyle', 'general']
        elif 'economics' in url:
            return ['economics', 'general']
        elif 'eco-ministries' in url:
            return ['economics', 'eco-ministry']
        elif 'bank-insurance' in url:
            return ['economics', 'bank-insurance']
        elif 'economic-others' in url:
            return ['economics', 'economic-others']
        elif 'literature' in url:
            return ['literature', 'general']
        elif 'probash' in url:
            return ['expatriate', 'general']
        elif 'crime' in url:
            return ['crime', 'general']

        # Check for pagination (if multiple pages)
        # next_page = response.css('a.next::attr(href)').get()  # Adjust based on the next page selector
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()