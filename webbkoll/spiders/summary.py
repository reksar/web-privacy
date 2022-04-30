from scrapy import Spider
from webbkoll.loaders import SummaryLoader


class SummarySpider(Spider):

    name = 'summary'
    summary = SummaryLoader()

    def __init__(self, **kwargs):
        super().__init__(self.name, **kwargs)
        self.start_urls = kwargs.get('urls', '').split()

    def parse(self, response):
        return self.summary(response)
