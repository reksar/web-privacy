import scrapy


class BriefSpider(scrapy.Spider):
    name = 'brief'
    allowed_domains = ['webbkoll.dataskydd.net']
    start_urls = ['http://webbkoll.dataskydd.net/']

    def parse(self, response):
        pass
