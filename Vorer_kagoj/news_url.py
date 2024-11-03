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
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Vorer_kagoj\\news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div.col-sm-4.col-md-4.paddingLR10.desktopSectionLead > div.thumbnail.marginB15 > a::attr(href), div.col-sm-8.col-md-8.paddingLR10.desktopSectionLead > div.thumbnail > a::attr(href), div.col-sm-12.col-md-12.lastItemNone > div.desktopSectionLead.marginB15 > div.thumbnail.borderRadius0.bgUnset.borderC1B1 > a::attr(href)')
        
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
        if 'government' in url:
            return ['natonal', 'government']
        elif 'law-justice' in url:
            return ['national', 'law-justice']
        elif 'media' in url:
            return ['national', 'media']
        elif 'accident' in url:
            return ['national', 'accident']
        elif 'mourning' in url:
            return ['national', 'mourning']
        elif 'weather' in url:
            return ['national', 'weather']
        elif 'national-other' in url:
            return ['national','national-other']
        elif 'country' in url:
            return ['national', 'whole-country']
        
        elif 'crime' in url:
            return ['crime', 'general']
        
        elif 'awamileague' in url:
            return ['politics', 'awamileague']
        elif 'bnp' in url:
            return ['politics', 'bnp']
        elif 'jp' in url:
            return ['politics', 'jp']
        elif 'jamat' in url:
            return ['politics', 'jamat']
        elif 'politics-other' in url:
            return ['politics', 'politics-other']
        elif 'worldtrade' in url:
            return ['economics', 'worldtrade']
        
        # International categories
        elif 'australia' in url:
            return ['international', 'australia']
        elif 'middleeast' in url:
            return ['international', 'middleeast']
        elif 'india' in url:
            return ['international', 'india']
        elif 'pakistan' in url:
            return ['international', 'pakistan']
        elif 'asia' in url:
            return ['international', 'asia']
        elif 'africa' in url:
            return ['international', 'africa']
        elif 'europe' in url:
            return ['international', 'europe']
        elif 'united-state' in url:
            return ['international', 'united-states']
        elif 'south-america' in url:
            return ['international', 'south-america']
        elif 'united-kingdom' in url:
            return ['international', 'united-kingdom']
        elif 'malaysia' in url:
            return ['international', 'malaysia']
        elif 'russia' in url:
            return ['international', 'russia']
        elif 'international-other' in url:
            return ['international', 'international-other']
        
        
        elif 'worldtrade' in url:
            return ['economics', 'worldtrade']
        elif 'corporate' in url:
            return ['economics', 'corporate']
        elif 'budget' in url:
            return ['economics', 'budget']
        elif 'export-import' in url:
            return ['economics', 'export-import']
        elif 'clothing' in url:
            return ['economics', 'clothing']
        elif 'share-market' in url:
            return ['economics', 'share-market']
        elif 'bank' in url:
            return ['economics', 'bank']
        elif 'insurance' in url:
            return ['economics', 'insurance']
        elif 'tourism' in url:
            return ['economics', 'tourism']
        elif 'revenue' in url:
            return ['economics', 'revenue']
        elif 'entrepreneur' in url:
            return ['economics', 'entrepreneur']
        elif 'private-org' in url:
            return ['economics', 'private-organization']
        elif 'economics-other' in url:
            return ['economics', 'economics-other']
        elif 'north-america' in url:
            return ['economics', 'north-america']
        elif 'business' in url:
            return ['economics', 'business']
            
        # Sports categories
        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'tennis' in url:
            return ['sports', 'tennis']
        elif 'hockey' in url:
            return ['sports', 'hockey']
        elif 'sports-interview' in url:
            return ['sports', 'interview']
        elif 'bpl' in url:
            return ['sports', 'bpl']
        elif 'ipl' in url:
            return ['sports', 'ipl']
        elif 'sports-other' in url:
            return ['sports', 'sports-other']
        
        # Entertainment categories
        elif 'dhallywood' in url:
            return ['entertainment', 'dhallywood']
        elif 'bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'tallywood' in url:
            return ['entertainment', 'tallywood']
        elif 'hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'drama' in url:
            return ['entertainment', 'drama']
        elif 'music' in url:
            return ['entertainment', 'music']
        elif 'entertainment-interview' in url:
            return ['entertainment', 'interview']
        elif 'entertainment-other' in url:
            return ['entertainment', 'other']
        
        elif 'makeup' in url:
            return ['lifestyle', 'makeup']
        elif 'home-decoration' in url:
            return ['lifestyle', 'home-decoration']
        elif 'fashion' in url:
            return ['lifestyle', 'fashion']
        elif 'tips' in url:
            return ['lifestyle', 'tips']
        elif 'solution' in url:
            return ['lifestyle', 'solution']
        elif 'food' in url:
            return ['lifestyle', 'food']
        elif 'lifestyle-other' in url:
            return ['lifestyle', 'other']
        
        elif 'admission' in url:
            return ['education', 'admission']
        elif 'exam' in url:
            return ['education', 'exam']
        elif 'result' in url:
            return ['education', 'result']
        elif 'scholarship' in url:
            return ['education', 'scholarship']
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'study-abroad' in url:
            return ['education', 'study-abroad']
        elif 'tutorial-other' in url:
            return ['education', 'other']

        elif 'tech-news' in url:
            return ['technology', 'tech-news']
        elif 'telecom' in url:
            return ['technology', 'telecom']
        elif 'mobile' in url:
            return ['technology', 'mobile']
        elif 'tech-socialmedia' in url:
            return ['technology', 'socialmedia']
        elif 'tech-apps' in url:
            return ['technology', 'apps']
        elif 'innovation' in url:
            return ['technology', 'innovation']
        elif 'freelancing' in url:
            return ['technology', 'freelancing']
        elif 'review' in url:
            return ['technology', 'review']
        elif 'tech-interview' in url:
            return ['technology', 'interview']
        elif 'tech-other' in url:
            return ['technology', 'other']
        
        elif 'opinion' in url:
            return ['opinion', 'general']
        
        elif 'health' in url:
            return ['health', 'general']

        elif 'science' in url:
            return ['science', 'general']

        elif '/lifestyle-travel' in url:
            return ['travel', 'general']
        elif '/travel' in url:
            return ['travel', 'general']
        
        elif 'probas' in url:
            return ['expatriate', 'general']
        
        elif 'prose' in url:
            return ['literature', 'prose']
        elif 'story' in url:
            return ['literature', 'story']
        elif 'poem' in url:
            return ['literature', 'poem']
        elif 'literature-interview' in url:
            return ['literature', 'interview']
        elif 'bookfair' in url:
            return ['literature', 'bookfair']
        elif 'book-discussion' in url:
            return ['literature', 'book-discussion']
        elif 'literature-other' in url:
            return ['literature', 'other']

        # Check for pagination (if multiple pages)
        # next_page = response.css('a.next::attr(href)').get()  # Adjust based on the next page selector
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()