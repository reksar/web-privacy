from scrapy import Spider, FormRequest
from webbkoll.loaders import SummaryLoader
from webbkoll.settings import WEBBKOLL_URL


class SummarySpider(Spider):
    name = 'summary'
    start_urls = [WEBBKOLL_URL]

    def parse(self, response):
        return FormRequest.from_response(
            response,
            # TODO: set URLs to parse.
            formdata={'url': 'http://smava.de'},
            callback=SummaryLoader(),
        )
