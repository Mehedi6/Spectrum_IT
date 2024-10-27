import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import pytz

class SeoSpider(scrapy.Spider):
    name = "seo_spider"

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'jugantor.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
    }

    def __init__(self, news_types=None, *args, **kwargs):
        super(SeoSpider, self).__init__(*args, **kwargs)
        self.news_types = news_types if news_types else []
        self.start_urls = self.get_start_urls()
        self.visited_urls = set()
    
    def get_start_urls(self):
        urls=[]
        if 'international' in self.news_types:
            urls += [
                'https://www.jugantor.com/northamerica',
                'https://www.jugantor.com/australian-continent',
                'https://www.jugantor.com/united-states',
                'https://www.jugantor.com/united-kingdom',
                'https://www.jugantor.com/middle-east',
                'https://www.jugantor.com/asia',
                'https://www.jugantor.com/europe',
                'https://www.jugantor.com/pakistan',
                'https://www.jugantor.com/malaysia',
                'https://www.jugantor.com/india',
                'https://www.jugantor.com/africa',
                'https://www.jugantor.com/southamerica',
                'https://www.jugantor.com/international-others',
                'https://www.jugantor.com/international',
            ]
        if 'economics' in self.news_types:
            urls += [
                'https://www.jugantor.com/budget',
                'https://www.jugantor.com/import-export',
                'https://www.jugantor.com/garments',
                'https://www.jugantor.com/share-market',
                'https://www.jugantor.com/bank',
                'https://www.jugantor.com/insurance',
                'https://www.jugantor.com/tourism',
                'https://www.jugantor.com/revenue',
                'https://www.jugantor.com/entrepreneur',
                'https://www.jugantor.com/economics-others',
                'https://www.jugantor.com/private-companies',
                'https://www.jugantor.com/economics',
            ]
        if 'national' in self.news_types:
            urls += [
                'https://www.jugantor.com/national',
                'https://www.jugantor.com/government',
                'https://www.jugantor.com/crime',
                'https://www.jugantor.com/law-justice',
                'https://www.jugantor.com/accident',
                'https://www.jugantor.com/mourning',
                'https://www.jugantor.com/national-others',
                'https://www.jugantor.com/media',
            ]
        if 'sports' in self.news_types:
            urls += [
                'https://www.jugantor.com/cricket',
                'https://www.jugantor.com/football',
                'https://www.jugantor.com/tenis',
                'https://www.jugantor.com/interview',
                'https://www.jugantor.com/sports-others',
                'https://www.jugantor.com/sports',
                    ]
        if 'politics' in self.news_types:
            urls += [
                'https://www.jugantor.com/bnp',
                'https://www.jugantor.com/awami-league',
                'https://www.jugantor.com/national-party',
                'https://www.jugantor.com/politics-others',
                'https://www.jugantor.com/politics',
            ]
        
        if 'lifestyle' in self.news_types:
            urls += [
                'https://www.jugantor.com/lifestyle',
                'https://www.jugantor.com/recipe',
                'https://www.jugantor.com/my-family',
                'https://www.jugantor.com/travel',
                'https://www.jugantor.com/solution',
                'https://www.jugantor.com/cooking',
                'https://www.jugantor.com/beauty',
                'https://www.jugantor.com/tips',
                'https://www.jugantor.com/lifestyle-others',
                'https://www.jugantor.com/news',
                'https://www.jugantor.com/legal-advice',

                
            ]
        
        if 'expatriate' in self.news_types:
            urls += [
                'https://www.jugantor.com/exile'
            ]
        
        if 'entertainment' in self.news_types:
            urls += [
                'https://www.jugantor.com/dhaliwood',
                'https://www.jugantor.com/bollywood',
                'https://www.jugantor.com/hollywood',
                'https://www.jugantor.com/entertainment-others',
                'https://www.jugantor.com/tollywood',
                'https://www.jugantor.com/song',
                'https://www.jugantor.com/entertainment-interview',
                'https://www.jugantor.com/drama',
            ]
        
        if 'interview' in self.news_types:
            urls += [
                'https://www.jugantor.com/interview',
            ]
        if 'tech' in self.news_types:
            urls += [
                'https://www.jugantor.com/tech',
                'https://www.jugantor.com/telco',
                'https://www.jugantor.com/mobile',
                'https://www.jugantor.com/it-social-media',
                'https://www.jugantor.com/apps',
                'https://www.jugantor.com/invantion',
                'https://www.jugantor.com/science',
                'https://www.jugantor.com/freelancing',
                'https://www.jugantor.com/reviews',
                'https://www.jugantor.com/tech-others',
                'https://www.jugantor.com/report',
                'https://www.jugantor.com/tech-interview'
            ]
        if 'education' in self.news_types:
            urls += [
                'https://www.jugantor.com/campus',
                'https://www.jugantor.com/tutorials',
                'https://www.jugantor.com/admission',
                'https://www.jugantor.com/exam',
                'https://www.jugantor.com/results',
                'https://www.jugantor.com/scholarship',
                'https://www.jugantor.com/campuses',
                'https://www.jugantor.com/study-abroad',
                'https://www.jugantor.com/campus-others',
            ]
        if 'job' in self.news_types:
            urls += [
                'https://www.jugantor.com/job-seek',
                'https://www.jugantor.com/govt-job',
                'https://www.jugantor.com/private-job',
                'https://www.jugantor.com/bank-insurance',
                'https://www.jugantor.com/state-org',
                'https://www.jugantor.com/defence',
                'https://www.jugantor.com/nternational-org',
                'https://www.jugantor.com/educational-institution',
                'https://www.jugantor.com/ngo',
                'https://www.jugantor.com/job-seek-media',
                'https://www.jugantor.com/ecruitment-exam',
                'https://www.jugantor.com/recruitment-exam-prep',
                'https://www.jugantor.com/job-seek-others',
            ]
        
        if 'literature' in self.news_types:
            urls += [
                'https://www.jugantor.com/literature',
                'https://www.jugantor.com/book-fair',
                'https://www.jugantor.com/prize',
                'https://www.jugantor.com/literature-others',
                'https://www.jugantor.com/prose',
                'https://www.jugantor.com/poem',
                'https://www.jugantor.com/literature-interview',
                'https://www.jugantor.com/book-discussion',
                'https://www.jugantor.com/news-of-the-art-literature',
                'https://www.jugantor.com/story',
            ]
        
        return urls

    def parse(self, response):
        

        for href in response.css('a::attr(href)').extract():
            url = response.urljoin(href)
            if 'international' in self.news_types:
                if '/international/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'international'})
                elif '/asia/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'asia'})
                elif '/northamerica/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'north-america'})
                elif '/southamerica/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'south-america'})
                elif '/australian-continent/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'australian-continent'})
                elif '/united-states/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'united-states'})
                elif '/united-kingdom/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'united-kingdom'})
                elif '/middle-east/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'middle-east'})
                elif '/europe/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'europe'})
                elif '/pakistan/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'pakistan'})
                elif '/malaysia/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'malaysia'})
                elif '/india/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'india'})
                elif '/africa/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'africa'})
                elif '/international-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'international-others'})
                
            if 'economics' in self.news_types:
                if '/economics/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'economics'})
                elif '/garments/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'garments'})

                elif '/budget/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'budget'})
                elif '/import-export/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'import-export'})
                elif '/share-market/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'share-market'})
                elif '/bank/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'bank'})
                elif '/insurance/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'insurance'})
                elif '/tourism/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tourism'})
                elif '/revenue/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'revenue'})
                elif '/entrepreneur/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'entrepreneur'})
                elif '/private-companies/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'private-companies'})
                elif '/economic-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'economic-others'})

            if 'sports' in self.news_types:
                if '/sports/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'sports'})
                elif '/cricket/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'cricket'})
                elif '/football/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'football'})
                elif '/tenis/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tenis'})
                elif '/sports-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'sports-others'})
                elif '/sports-interview/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'sports-interview'})
            
            if 'politics' in self.news_types:
                if '/politics/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'politics'})
                elif '/bnp/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'bnp'})
                elif '/awami-league/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'awami-league'})
                elif '/national-party/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'national-party'})
                elif '/jamaat/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'jamaat'})
                elif '/politics-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'politics-others'})
            
            if 'national' in self.news_types:
                if '/national/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'national'})
                elif '/government/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'government'})
                elif '/law-justice/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'law-justice'})
                elif '/accident/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'accident'})
                elif '/mourning/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'mourning'})
                elif '/national-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'national-others'})
                elif '/media/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'media'})
            if 'lifestyle' in self.news_types:
                if '/lifestyle/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'lifestyle'})
                elif '/recipe/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'recipe'})
                elif '/my-family/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'my-family'})
                elif '/beauty/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'beauty'})
                elif '/solution/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'solution'})
                elif '/cooking/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'cooking'})
                elif '/tips/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tips'})
                elif '/lifestyle-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'lifestyle-others'})
                elif '/news/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'news'})
                elif '/legal-advice/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'legal-advice'})
            
            if '/travel/' in url and url not in self.visited_urls:
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'travel'})
            
            if '/exile/' in url and url not in self.visited_urls:
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'expatriate'})
            
            if 'entertainment' in self.news_types:
                if '/entertainment/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'entertainment'})
                
                elif '/dhaliwood/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'dhaliwood'})
                elif '/bollywood/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'bollywood'})
                elif '/hollywood/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'hollywood'})
                elif '/entertainment-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'entertainment-others'})
                elif '/tollywood/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tollywood'})
                elif '/song/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'song'})
                elif '/entertainment-interview/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'entertainment-interview'})
                elif '/drama/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'drama'})
            if '/interview/' in url and url not in self.visited_urls:
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'interview'})

            if 'tech' in self.news_types:
                if '/tech/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tech'})
                
                elif '/telco/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'telco'})
                elif '/mobile/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'mobile'})
                elif '/it-social-media/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'it-social-media'})
                elif '/apps/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'apps'})
                elif '/invantion/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'invantion'})
                elif '/science/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'science'})
                elif '/freelancing/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'freelancing'})
                elif '/reviews/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'reviews'}) 
                elif '/tech-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tech-others'})
                elif '/report/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'report'})
                elif '/tech-interview/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tech-interview'})
            if '/crime/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'crime'})

            if 'education' in self.news_types:
                if '/campus/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'campus'})
                
                elif '/tutorials/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'tutorials'})
                elif '/admission/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'admission'})
                elif '/exam/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'exam'})
                elif '/results/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'results'})
                elif '/scholarship/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'scholarship'})
                elif '/campuses/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'campuses'})
                elif '/study-abroad/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'study-abroad'})
                elif '/campus-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'campus-others'}) 
            if 'job' in self.news_types:
                if '/job-seek/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'job-seek'})
                
                elif '/govt-job/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'govt-job'})
                elif '/private-job/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'private-job'})
                elif '/bank-insurance/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'bank-insurance'})
                elif '/state-org/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'state-org'})
                elif '/defence/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'defence'})
                elif '/nternational-org/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'international-org'})
                elif '/educational-institution/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'educational-institution'})
                elif '/ngo/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'ngo'}) 
                elif '/job-seek-media/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'job-seek-media'})
                elif '/ecruitment-exam/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'recruitment-exam'})
                elif '/recruitment-exam-prep/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'recruitment-exam-prep'})
                elif '/job-seek-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'recruitment-exam-prep'})
            if 'literature' in self.news_types:
                if '/literature/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'literature'})
                
                elif '/book-fair/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'book-fair'})
                elif '/prize/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'prize'})
                elif '/literature-others/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'literature-others'})
                elif '/book-discussion/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'book-discussion'})
                elif '/news-of-the-art-literature/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'news-of-the-art-literature'})
                elif '/story/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'story'})
                elif '/prose/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'prose'})
                elif '/poem/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'poem'}) 
                elif '/job-seek-media/' in url and url not in self.visited_urls:
                    self.visited_urls.add(url)
                    yield scrapy.Request(url, callback=self.parse_page, meta={'subcategory': 'job-seek-media'})          
                

                
               
    def parse_page(self, response):
        page_data = {
            'url': response.url,
            'title': response.css('title::text').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get(),
            'published_date': self.extract_date(response),
            'updated_date': None,
            'news_type': self.get_news_type(response.url),
            'news_subcategory': response.meta.get('subcategory', 'general'),
            'media_type': 'newspaper',
            'image_urls': (self.extract_image_urls(response))[0] if self.extract_image_urls(response) else None,
            'keywords': self.extract_keywords(response),
            'last_scraped': datetime.now(pytz.timezone('Asia/Dhaka')).isoformat(),
            'source': "যুগান্তর",
            'international': True if self.get_news_type(response.url)=="international" else False,
            'old': False,
            'sentiment': 'neutral',
            'views': 0,
            'news_score': 0,
            'rating': 0,
            'engagement': 0,
            'author': self.extract_author(response),
            'content': self.extract_content(response),
            
        }
        self.log(f"Extracted data: {page_data}")  # Log the extracted data for debugging
        yield page_data

    # Bengali to English date conversion and replacement methods
    def bengali_to_english(self, bengali_str):
        bengali_to_english_digits = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        return bengali_str.translate(bengali_to_english_digits)

    def replace_bengali_strings(self, english_date_str):
        month_replacements = {
            'জানুয়ারি': 'January',
            'ফেব্রুয়ারি': 'February',
            'মার্চ': 'March',
            'এপ্রিল': 'April',
            'মে': 'May',
            'জুন': 'June',
            'জুলাই': 'July',
            'আগস্ট': 'August',
            'সেপ্টেম্বর': 'September',
            'অক্টোবর': 'October',
            'নভেম্বর': 'November',
            'ডিসেম্বর': 'December'
        }

        for bengali_month, english_month in month_replacements.items():
            english_date_str = english_date_str.replace(bengali_month, english_month)

        english_date_str = english_date_str.replace('এএম', 'AM').replace('পিএম', 'PM')
        return english_date_str

    def parse_bengali_date(self, bengali_date_str):
        bengali_date_str = bengali_date_str.replace('প্রকাশ: ', '').strip()
        english_date_str = self.bengali_to_english(bengali_date_str)
        english_date_str = self.replace_bengali_strings(english_date_str)

        try:
            return datetime.strptime(english_date_str, "%d %B %Y, %I:%M %p")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None

    # Extracting date from the page
    def extract_date(self, response):
        date_xpath = "//p[@class='desktopDetailPTime color1']/text()"
        date_text = response.xpath(date_xpath).get()
        if date_text:
            return self.parse_bengali_date(date_text)
        return None

    # Extracting author from the page
    def extract_author(self, response):
        author_tag = response.css("p.desktopDetailReporter::text").get()
        return author_tag.strip() if author_tag else None

    # Extracting content from the page
    def extract_content(self, response):
        content_div = response.css("div.desktopDetailBody p::text").extract()
        content = '\n'.join([p.strip() for p in content_div])
        return content if content else None

    # Extracting image URLs from the page
    def extract_image_urls(self, response):
        image_xpath = "//div[contains(@class, 'desktopDetailPhotoDiv')]//figure//img/@src"
        image_urls = response.xpath(image_xpath).extract()
        return [response.urljoin(img_url) for img_url in image_urls]

    # Extracting keywords from the meta tags
    def extract_keywords(self, response):
        keywords = response.css('meta[name="keywords"]::attr(content)').get()
        return [kw.strip() for kw in keywords.split(',')] if keywords else None

    # Determine the news type from URL
    def get_news_type(self, url):
        if 'asia' in url or 'international' in url or 'europe' in url or 'northamerica' in url or 'southamerica' in url or 'australian-continent' in url or 'malaysia' in url or 'united-states' in url or 'united-kingdom' in url or 'middle-east' in url or 'pakistan' in url or 'india' in url or 'africa' in url or 'international-others' in url:
            return 'international'
        
        if 'economics' in url or 'garments' in url or 'budget' in url or 'share-market' in url or 'tourism' in url or 'revenue' in url or 'import-export' in url or 'bank' in url or 'insurance' in url or 'entrepreneur' in url or 'private-companies' in url or 'economics-others' in url:
            return 'economics'
        
        if ('sports' in url) or ('cricket' in url) or ('football' in url) or ('tenis' in url) or ('sports-interview' in url) or ('sports-others' in url):
            return 'sports'
        
        if ('bnp' in url) or ('awami-league' in url) or ('national-party' in url) or ('jamaat' in url) or ('politics-others' in url):
            return 'politics'
        
        if ('national' in url) or ('government' in url) or ('law-justice' in url) or ('accident' in url) or ('mourning' in url) or ('national-others' in url) or ('media' in url):
            return 'national'
        
        if ('lifestyle' in url) or ('recipe' in url) or ('my-family' in url) or ('travel' in url) or ('solution' in url) or ('cooking' in url) or ('beauty' in url) or ('tips' in url) or ('lifestyle-others' in url) or ('news' in url) or ('legal-advice' in url):
            return 'lifestyle'
       
        if ('travel' in url):
            return 'travel'

        if ('exile' in url):
            return 'expatriate'
        
        if ('entertainment' in url) or ('dhaliwood' in url) or ('bollywood' in url) or ('tollywood' in url) or ('hollywood' in url) or ('entertainment-others' in url) or ('song' in url) or ('drama' in url) or ('entertainment-interview' in url):
            return 'entertainment'

        if ('interview' in url):
            return 'interview'
        
        if ('tech' in url) or ('telco' in url) or ('mobile' in url) or ('it-social-media' in url) or ('apps' in url) or ('invantion' in url) or ('science' in url) or ('freelancing' in url) or ('reviews' in url) or ('tech-others' in url) or ('report' in url) or ('tech-interview' in url):
            return 'tech'
        
        if ('crime' in url):
            return 'crime'
        
        if ('campus' in url) or ('tutorials' in url) or ('admission' in url) or ('exam' in url) or ('results' in url) or ('scholarship' in url) or ('campuses' in url) or ('study-abroad' in url) or ('campus-others' in url):
            return 'education'
        
        if ('job-seek' in url) or ('govt-job' in url) or ('private-job' in url) or ('bank-insurance' in url) or ('state-org' in url) or ('defence' in url) or ('nternational-org' in url) or ('educational-institution' in url) or ('ngo' in url) or ('ecruitment-exam' in url) or ('recruitment-exam-prep' in url) or ('job-seek-media' in url) or ('job-seek-others' in url):
            return 'job'
        
        if ('literature' in url) or ('book-fair' in url) or ('prize' in url) or ('literature-others' in url) or ('prose' in url) or ('poem' in url) or ('literature-interview' in url) or ('book-discussion' in url) or ('news-of-the-art-literature' in url) or ('story' in url):
            return 'literature'
process = CrawlerProcess()
process.crawl(SeoSpider, news_types = ['economics', 'international','sports','politics','national','crime','lifestyle','travel','expatriate','entertainment','interview','tech','education','job','literature'])
process.start()
