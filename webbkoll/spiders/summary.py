from scrapy import Spider
from webbkoll.loaders import SummaryLoader


class SummarySpider(Spider):

    name = 'summary'
    summary = SummaryLoader()

    start_urls = [
        'http://smava.de',
        'https://boyter.org/2016/04/collection-orly-book-covers',
        'http://docs.python.org',
    ]

    def parse(self, response):
        return self.summary(response)
