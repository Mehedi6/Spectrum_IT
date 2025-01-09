import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    visited_urls = []
    start_urls = [

        #national
        'https://www.dailynayadiganta.com/law-and-justice/4',
        'https://www.dailynayadiganta.com/diplomacy/21',
        'https://www.dailynayadiganta.com/administration/27',
        'https://www.dailynayadiganta.com/Incident-accident/6',
        'https://www.dailynayadiganta.com/organization/23',
        'https://www.dailynayadiganta.com/parliament/24',
        'https://www.dailynayadiganta.com/election/25',
        'https://www.dailynayadiganta.com/miscellaneous/26',
        'https://www.dailynayadiganta.com/khulna/42',
        'https://www.dailynayadiganta.com/barishal/43',
        'https://www.dailynayadiganta.com/sylhet/44',
        'https://www.dailynayadiganta.com/rangpur/45',
        'https://www.dailynayadiganta.com/mymensingh/46',
        'https://www.dailynayadiganta.com/rajshahi/41',
        'https://www.dailynayadiganta.com/chattagram/40',
        'https://www.dailynayadiganta.com/dhaka/39',
        #economics
        'https://www.dailynayadiganta.com/economics/3',
        #politics
        'https://www.dailynayadiganta.com/politics/2',   
        #crime
        'https://www.dailynayadiganta.com/crime/5',
        #education
        'https://www.dailynayadiganta.com/education/22',
        #international
        'https://www.dailynayadiganta.com/subcontinent/28',
        'https://www.dailynayadiganta.com/asia/29',
        'https://www.dailynayadiganta.com/middle-east/30',
        'https://www.dailynayadiganta.com/turkey/31',
        'https://www.dailynayadiganta.com/usa-canada/32',
        'https://www.dailynayadiganta.com/america/33',
        'https://www.dailynayadiganta.com/europe/34',
        'https://www.dailynayadiganta.com/africa/35',
        'https://www.dailynayadiganta.com/australia/36',
        'https://www.dailynayadiganta.com/international-organizations/37',
        'https://www.dailynayadiganta.com/miscellaneous/38',
        #sports
        'https://www.dailynayadiganta.com/athletics/52',
        'https://www.dailynayadiganta.com/tennis/51',
        'https://www.dailynayadiganta.com/hockey/47',
        'https://www.dailynayadiganta.com/cricket/48',
        'https://www.dailynayadiganta.com/football/49',
        'https://www.dailynayadiganta.com/swimming/50',
        'https://www.dailynayadiganta.com/miscellaneous/53',
        #opinion
        'https://www.dailynayadiganta.com/opinion/10',
        #health
        'https://www.dailynayadiganta.com/health/60',
        #travel
        'https://www.dailynayadiganta.com/travel/65',
        #lifestyle
        'https://www.dailynayadiganta.com/fashion/61',
        'https://www.dailynayadiganta.com/parenting/62',
        'https://www.dailynayadiganta.com/housekeeping/63',
        'https://www.dailynayadiganta.com/Cooking/64',
        'https://www.dailynayadiganta.com/miscellaneous/66',
        #ent
        'https://www.dailynayadiganta.com/cinema/54',
        'https://www.dailynayadiganta.com/television/55',
        'https://www.dailynayadiganta.com/radio/56',
        'https://www.dailynayadiganta.com/natok/57',
        'https://www.dailynayadiganta.com/music/58',
        'https://www.dailynayadiganta.com/miscellaneous/59',
        #lit
        'https://www.dailynayadiganta.com/poetry/74',
        'https://www.dailynayadiganta.com/story/75',
        'https://www.dailynayadiganta.com/novel/76',
        'https://www.dailynayadiganta.com/classic/77',
        'https://www.dailynayadiganta.com/discussion/78',
        'https://www.dailynayadiganta.com/miscellaneous/79',



    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\NayaDigonto\\news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div.col-md-8.col-sm-8.col-xs-7.column-no-left-padding > a::attr(href)')
        
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
        # Mapping URLs to categories based on URL patterns
        if '/law-and-justice/' in url:
            return ['national', 'law-justice']
        if '/diplomacy/' in url: 
            return ['national', 'diplomacy'] 
        elif '/administration/' in url: 
            return ['national', 'administration'] 
        elif '/Incident-accident/' in url: 
            return ['national', 'incident-accident'] 
        elif '/organization/' in url: 
            return ['national', 'organization'] 
        elif '/parliament/' in url: 
            return ['national', 'parliament'] 
        elif '/election/' in url: 
            return ['national', 'election'] 
        elif '/miscellaneous/' in url: 
            return ['national', 'miscellaneous'] 
        elif '/khulna/' in url: 
            return ['national', 'khulna'] 
        elif '/barishal/' in url: 
            return ['national', 'barishal'] 
        elif '/sylhet/' in url: 
            return ['national', 'sylhet'] 
        elif '/rangpur/' in url: 
            return ['national', 'rangpur'] 
        elif '/mymensingh/' in url: 
            return ['national', 'mymensingh'] 
        elif '/rajshahi/' in url: 
            return ['national', 'rajshahi'] 
        elif '/chattagram/' in url: 
            return ['national', 'chattagram'] 
        elif '/dhaka/' in url: 
            return ['national', 'dhaka'] 
        elif '/economics/' in url: 
            return ['economics', 'general'] 
        elif '/politics/' in url: 
            return ['politics','general'] 
        elif '/crime/' in url: 
            return ['crime','general'] 
        elif '/education/' in url: 
            return ['education','general'] 
        elif '/subcontinent/' in url: 
            return ['international', 'subcontinent'] 
        elif '/asia/' in url: 
            return ['international', 'asia'] 
        elif '/middle-east/' in url: 
            return ['international', 'middle-east'] 
        elif '/turkey/' in url: 
            return ['international', 'turkey'] 
        elif '/usa-canada/' in url: 
            return ['international', 'usa-canada'] 
        elif '/america/' in url: 
            return ['international', 'america'] 
        elif '/europe/' in url: 
            return ['international', 'europe'] 
        elif '/africa/' in url: 
            return ['international', 'africa'] 
        elif '/australia/' in url: 
            return ['international', 'australia'] 
        elif '/international-organizations/' in url: 
            return ['international', 'international-organizations'] 
        elif '/athletics/' in url: 
            return ['sports', 'athletics'] 
        elif '/tennis/' in url: 
            return ['sports', 'tennis'] 
        elif '/hockey/' in url: 
            return ['sports', 'hockey'] 
        elif '/cricket/' in url: 
            return ['sports', 'cricket'] 
        elif '/football/' in url: 
            return ['sports', 'football'] 
        elif '/swimming/' in url: 
            return ['sports', 'swimming'] 
        elif '/opinion/' in url: 
            return ['opinion','general'] 
        elif '/health/' in url: 
            return ['health','general'] 
        elif '/travel/' in url: 
            return ['travel', 'general'] 
        elif '/fashion/' in url: 
            return ['lifestyle', 'fashion'] 
        elif '/parenting/' in url: 
            return ['lifestyle', 'parenting'] 
        elif '/housekeeping/' in url: 
            return ['lifestyle', 'housekeeping'] 
        elif '/Cooking/' in url: 
            return ['lifestyle', 'cooking'] 
        elif '/cinema/' in url: 
            return ['entertainment', 'cinema'] 
        elif '/television/' in url: 
            return ['entertainment', 'television'] 
        elif '/radio/' in url: 
            return ['entertainment', 'radio'] 
        elif '/natok/' in url: 
            return ['entertainment', 'natok'] 
        elif '/music/' in url: 
            return ['entertainment', 'music'] 
        elif '/poetry/' in url: 
            return ['literature', 'poetry'] 
        elif '/story/' in url: 
            return ['literature', 'story'] 
        elif '/novel/' in url: 
            return ['literature', 'novel'] 
        elif '/classic/' in url: 
            return ['literature', 'classic'] 
        elif '/discussion/' in url: 
            return ['literature', 'discussion'] 
        else:
            return [None, None]
        

        # Check for pagination (if multiple pages)
        # next_page = response.css('a.next::attr(href)').get()  # Adjust based on the next page selector
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()