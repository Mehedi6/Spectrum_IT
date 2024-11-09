import scrapy
from scrapy.crawler import CrawlerProcess

class LinkSpider(scrapy.Spider):

    name = "link_spider"
    visited_urls = []
    start_urls = [

        #national
        'https://www.kalbela.com/national',
        'https://www.kalbela.com/country-news/dhaka',
        'https://www.kalbela.com/country-news/chittagong',
        'https://www.kalbela.com/country-news/rajshahi',
        'https://www.kalbela.com/country-news/khulna',
        'https://www.kalbela.com/country-news/barisal',
        'https://www.kalbela.com/country-news/sylhet',
        'https://www.kalbela.com/country-news/rangpur',
        'https://www.kalbela.com/country-news/mymensingh',
        'https://www.kalbela.com/capital',
        'https://www.kalbela.com/environment-climate'
        #politics
        'https://www.kalbela.com/politics',
        #international
        'https://www.kalbela.com/world/middle-east',
        'https://www.kalbela.com/world/united-states',
        'https://www.kalbela.com/world/europe',
        'https://www.kalbela.com/world/asia',
        'https://www.kalbela.com/world/india',
        'https://www.kalbela.com/world/united-kingdom',
        'https://www.kalbela.com/world/pakistan',
        'https://www.kalbela.com/world/malaysia',
        'https://www.kalbela.com/world/north-america',
        'https://www.kalbela.com/world/south-america',
        'https://www.kalbela.com/world/africa',
        'https://www.kalbela.com/world/others',
        #sports
        'https://www.kalbela.com/sports/cricket',
        'https://www.kalbela.com/sports/football',
        'https://www.kalbela.com/sports/others',
        #entertainment
        'https://www.kalbela.com/entertainment/bollywood',
        'https://www.kalbela.com/entertainment/hollywood',
        'https://www.kalbela.com/entertainment/tollywood',
        'https://www.kalbela.com/entertainment/dhallywood',
        'https://www.kalbela.com/entertainment/others',
        #education
        'https://www.kalbela.com/dainikshiksha/campus',
        'https://www.kalbela.com/dainikshiksha/admission',
        'https://www.kalbela.com/dainikshiksha/exam',
        'https://www.kalbela.com/dainikshiksha/results',
        'https://www.kalbela.com/dainikshiksha/others',
        #economics
        'https://www.kalbela.com/business-news',
        'https://www.kalbela.com/corporate',
        #health
        'https://www.kalbela.com/health/health-care',
        'https://www.kalbela.com/health/health-education',
        'https://www.kalbela.com/health/treatment',
        'https://www.kalbela.com/health/disease',
        'https://www.kalbela.com/health/health-query',
        'https://www.kalbela.com/health/others',
        #expatriate
        'https://www.kalbela.com/probash',
        #crime
        'https://www.kalbela.com/legal-advice',
        'https://www.kalbela.com/court-law',
        'https://www.kalbela.com/crime',
        #lifestyle
        'https://www.kalbela.com/lifestyle/fashion',
        'https://www.kalbela.com/lifestyle/make-up',
        'https://www.kalbela.com/lifestyle/home-decoration',
        'https://www.kalbela.com/lifestyle/jewellery',
        'https://www.kalbela.com/lifestyle/food',
        'https://www.kalbela.com/lifestyle/others',
        #opinion
        'https://www.kalbela.com/opinion/interview',
        'https://www.kalbela.com/opinion/editorial',
        'https://www.kalbela.com/opinion/sub-editorial',
        'https://www.kalbela.com/opinion/reaction',
        'https://www.kalbela.com/opinion/remembrance',
        'https://www.kalbela.com/opinion/letter',
        'https://www.kalbela.com/opinion/book-review',
        'https://www.kalbela.com/opinion/readers-voice',
        'https://www.kalbela.com/opinion/others',
        #technology
        'https://www.kalbela.com/technology/gadget',
        'https://www.kalbela.com/technology/mobile',
        'https://www.kalbela.com/technology/apps',
        'https://www.kalbela.com/technology/telecom',
        'https://www.kalbela.com/technology/computer',
        'https://www.kalbela.com/technology/tips',
        'https://www.kalbela.com/technology/freelancing',
        'https://www.kalbela.com/technology/others',
        #science
        'https://www.kalbela.com/technology/science',
        #literature
        'https://www.kalbela.com/art-literature/poem',
        'https://www.kalbela.com/art-literature/literature',
        'https://www.kalbela.com/art-literature/others',
        #jobs
        'https://www.kalbela.com/job-news',


        
        


    ]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'C:\\Users\\arwen\\Desktop\\Newspaper Scraping\\Spectrum_IT\\Kalbela\\news_url.json',
        'FEED_EXPORT_INDENT': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,  # Limit to one request at a time
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEFAULT': str,
        
    }


    def parse(self, response):
        # Extract all news articles on the page 
        
        # news_items_1 = response.css('div.info.has_ai > div > div.title_holder > div > h2 > a')  # Adjust the selector based on the HTML structure
        news_items_2 =response.css('div.sub-news> a::attr(href), div.common-card-content.position-relative > div.image-lead.position-relative.text-center > a::attr(href)')
        
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
        elif 'capital' in url or 'dhaka' in url:
            return ['national', 'capital-city']
        elif 'chittagong' in url:
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
        elif 'environment-climate' in url:
            return ['national', 'environment-climate']
        elif 'legal-advice' in url:
            return ['national', 'legal-advice']
        elif 'court-law' in url:
            return ['national', 'court-law']
        
        elif 'politics' in url:
            return ['politics', 'general']
        
        elif 'middle-east' in url:
            return ['international', 'middle-east']
        elif 'united-states' in url:
            return ['international', 'united-states']
        elif 'europe' in url:
            return ['international', 'europe']
        elif 'asia' in url:
            return ['international', 'asia']
        elif 'india' in url:
            return ['international', 'india']
        elif 'united-kingdom' in url:
            return ['international', 'united-kingdom']
        elif 'pakistan' in url:
            return ['international', 'pakistan']
        elif 'malaysia' in url:
            return ['international', 'malaysia']
        elif 'north-america' in url:
            return ['international', 'north-america']
        elif 'south-america' in url:
            return ['international', 'south-america']
        elif 'africa' in url:
            return ['international', 'africa']
        elif 'world/others' in url:
            return ['international', 'general']
        
        elif 'cricket' in url:
            return ['sports', 'cricket']
        elif 'football' in url:
            return ['sports', 'football']
        elif 'sports/others' in url:
            return ['sports', 'general']
        
        if 'bollywood' in url:
            return ['entertainment', 'bollywood']
        elif 'hollywood' in url:
            return ['entertainment', 'hollywood']
        elif 'tollywood' in url:
            return ['entertainment', 'tollywood']
        elif 'dhallywood' in url:
            return ['entertainment', 'dhallywood']
        elif 'entertainment/others' in url:
            return ['entertainment', 'others']
        
        elif 'campus' in url:
            return ['education', 'campus']
        elif 'admission' in url:
            return ['education', 'admission']
        elif 'exam' in url:
            return ['education', 'exam']
        elif 'results' in url:
            return ['education', 'results']
        elif 'dainikshiksha/others' in url:
            return ['education', 'general']
        
        # Economics
        elif 'business-news' in url:
            return ['economics', 'business-news']
        elif 'corporate' in url:
            return ['economics', 'corporate']
        
        # Health
        elif 'health-care' in url:
            return ['health', 'health-care']
        elif 'health-education' in url:
            return ['health', 'health-education']
        elif 'treatment' in url:
            return ['health', 'treatment']
        elif 'disease' in url:
            return ['health', 'disease']
        elif 'health-query' in url:
            return ['health', 'health-query']
        elif 'health/others' in url:
            return ['health', 'general']
        
        # Expatriate
        elif 'probash' in url:
            return ['expatriate', 'general']
        
        # Crime
    
        elif 'crime' in url:
            return ['crime', 'general']
        
        # Lifestyle
        elif 'fashion' in url:
            return ['lifestyle', 'fashion']
        elif 'make-up' in url:
            return ['lifestyle', 'make-up']
        elif 'home-decoration' in url:
            return ['lifestyle', 'home-decoration']
        elif 'jewellery' in url:
            return ['lifestyle', 'jewellery']
        elif 'food' in url:
            return ['lifestyle', 'food']
        elif 'lifestyle/others' in url:
            return ['lifestyle', 'general']
        
        # Opinion
        elif 'interview' in url:
            return ['opinion', 'interview']
        elif 'editorial' in url:
            return ['opinion', 'editorial']
        elif 'sub-editorial' in url:
            return ['opinion', 'sub-editorial']
        elif 'reaction' in url:
            return ['opinion', 'reaction']
        elif 'remembrance' in url:
            return ['opinion', 'remembrance']
        elif 'letter' in url:
            return ['opinion', 'letter']
        elif 'book-review' in url:
            return ['opinion', 'book-review']
        elif 'readers-voice' in url:
            return ['opinion', 'readers-voice']
        elif 'opinion/others' in url:
            return ['opinion', 'general']
        
       
        elif 'gadget' in url:
            return ['technology', 'gadget']
        elif 'mobile' in url:
            return ['technology', 'mobile']
        elif 'apps' in url:
            return ['technology', 'apps']
        elif 'telecom' in url:
            return ['technology', 'telecom']
        elif 'computer' in url:
            return ['technology', 'computer']
        elif 'tips' in url:
            return ['technology', 'tips']
        elif 'freelancing' in url:
            return ['technology', 'freelancing']
        elif 'technology/others' in url:
            return ['technology', 'general']
        
        # Science
        elif 'science' in url:
            return ['science', 'general']
        
        # Literature
        elif 'poem' in url:
            return ['literature', 'poem']
        elif 'literature' in url:
            return ['literature', 'literature']
        elif 'art-literature/others' in url:
            return ['literature', 'general']
        
        # Jobs
        elif 'job-news' in url:
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