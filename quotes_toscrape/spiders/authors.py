import scrapy
import datetime

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        # 'CONCURRENT_REQUESTS': 50,
        # 'DOWNLOAD_DELAY': 0.1,
        'FEED_URI': f'output/authors_{datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ('name','birth_date','birth_location','description',) 
    }

    def parse(self, response):
        for _ in response.xpath("//div[@class='quote']"):
            author_page = response.xpath("//a[text()='(about)']/@href").get()
            yield response.follow(author_page, callback=self.parse_author)

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)


    def parse_author(self, response):
        print("------------------------------------")
        yield {
            'name': response.xpath("//h3[@class='author-title']/text()").get(),
            'birth_date': response.xpath("//span[@class='author-born-date']/text()").get(),
            'birth_location': response.xpath("//span[@class='author-born-location']/text()").get(),
            'description': response.xpath("//div[@class='author-description']/text()").get()
        }



