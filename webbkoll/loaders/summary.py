from scrapy.selector import Selector
from itemloaders.processors import TakeFirst
from webbkoll.items import Summary
from .common import summary_li, select_css
from . import DataclassLoader, CookiesLoader, AsideRequestsLoader


ASIDE_REQUESTS = AsideRequestsLoader()
COOKIES = CookiesLoader()
TAKE_FIRST = TakeFirst()

IP = '.'.join(['\d{1,3}'] * 4)


class SummaryLoader(DataclassLoader):

    @property
    def dataclass(self):
        return Summary

    def summary_url(self):
        return self.response.url

    @select_css
    def checked_url(self):
        return '.url li:first-child a::text'

    @select_css
    def final_url(self):
        return '.url li:last-child a::text'

    def ip(self):
        return self.summary_li(6).re_first(IP)

    def default_https(self):
        return is_success(self.summary_li(1))

    def cookies(self):
        return COOKIES(self.css_response(summary_li(4)))

    def aside_requests(self):
        return ASIDE_REQUESTS(self.css_response(summary_li(5)))

    def csp(self):
        return is_success(self.summary_li(2))

    def referrer_policy(self):
        return is_success(self.summary_li(3))

    def summary_li(self, nth):
        return TAKE_FIRST(self.response.css(summary_li(nth)))


def is_success(li: Selector):
    return 'success' in li.css('i').attrib['class']
