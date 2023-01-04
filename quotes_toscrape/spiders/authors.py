import scrapy
import datetime
class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'CONCURRENT_REQUESTS': 50,
        'DOWNLOAD_DELAY': 0.1,
        'FEED_URI': f'output/authors_{datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ('name','birth_date','birth_location','description',) 
    }

    def parse(self, response):
        for author in response.xpath("//div[@class='quote']/span/a/@href").getall():
            yield scrapy.Request(response.urljoin(author)+'/',
                                method="GET",
                                callback=self.parse_author,
                                headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'})

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)


    def parse_author(self, response):
        yield {
            'name': response.xpath("//h3[@class='author-title']/text()").get(),
            'birth_date': response.xpath("//span[@class='author-born-date']/text()").get(),
            'birth_location': response.xpath("//span[@class='author-born-location']/text()").get(),
            'description': response.xpath("//div[@class='author-description']/text()").get()
        }