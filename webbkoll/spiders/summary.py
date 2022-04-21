from scrapy import Spider, FormRequest
from scrapy.http import Request, Response
from webbkoll.loaders import SummaryLoader
from webbkoll.settings import WEBBKOLL_URL


class SummarySpider(Spider):
    name = 'summary'
    summary = SummaryLoader()
    start_urls = ['http://smava.de']

    def start_requests(self):
        yield from map(webbkoll_check, self.start_urls)

    def parse(self, response):
        return self.summary(response)


def webbkoll_check(url):
    return Request(WEBBKOLL_URL,
        callback=submit_check_form,
        cb_kwargs={'url': url},
        dont_filter=True)

def submit_check_form(check_form: Response, **form_data: dict) -> Request:
    return FormRequest.from_response(
        check_form,
        formdata=form_data,
        dont_filter=True)
