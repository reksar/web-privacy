from scrapy import Spider, FormRequest
from webbkoll.loaders import SummaryLoader


class SummarySpider(Spider):
    name = 'summary'
    start_urls = ['https://webbkoll.dataskydd.net/']

    def parse(self, response):
        return FormRequest.from_response(
            response,
            formdata={'url': 'http://smava.de'},
            callback=SummaryLoader(),
        )
