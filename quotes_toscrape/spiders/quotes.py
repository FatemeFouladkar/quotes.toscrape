import scrapy
import datetime


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    custom_settings = {
        'CONCURRENT_REQUESTS': 50,
        'DOWNLOAD_DELAY': 0.1,
        'FEED_URI': f'output/quotes_{datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ('text', 'author', 'tags') 
    }

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath(".//span[@class='text']/text()").get(),
                'author': quote.xpath(".//small[@class='author']/text()").get(),
                'tags': quote.xpath(".//a[@class='tag']/text()").getall(),
                }
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)
