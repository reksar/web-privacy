from scrapy import Spider
from scrapy.exceptions import DropItem
from webbkoll.loaders import SummaryLoader
from webbkoll.items import WebbkollError
from w3lib.html import remove_tags


class SummarySpider(Spider):

    name = 'summary'
    summary = SummaryLoader()

    def __init__(self, **kwargs):
        super().__init__(self.name, **kwargs)
        self.start_urls = kwargs.get('urls', '').split()

    def parse(self, response):

        if has_summary(response):
            return self.summary(response)

        message = error_message(response)
        if message:
            return WebbkollError(message)

        raise DropItem('Summary parsing error')


def has_summary(response):
    return bool(len(response.css('#results-header')))


def error_message(response):
    return remove_tags(response.css('.text').re_first('<p>Error:.*</p>'))
