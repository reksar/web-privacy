from scrapy.selector import Selector
from webbkoll.items import SummaryItem
from .dataclass import DataclassLoader
from .cookies import CookiesLoader
from .aside_requests import AsideRequestsLoader
from .common import select_css, summary_li, find, TAKE_FIRST


IP = '.'.join(['\d{1,3}'] * 4)
COOKIES = CookiesLoader()
ASIDE_REQUESTS = AsideRequestsLoader()


class SummaryLoader(DataclassLoader):

    @property
    def dataclass(self):
        return SummaryItem

    def summary_url(self):
        return self.response.url

    @select_css
    def checked_url(self):
        return '.url li:first-child a::text'

    @select_css
    def final_url(self):
        return '.url li:last-child a::text'

    def ip(self):
        return find(IP, TAKE_FIRST(self.response.css(summary_li(6))))

    def default_https(self):
        return is_success(TAKE_FIRST(self.response.css(summary_li(1))))

    def cookies(self):
        return COOKIES(self.css_response(summary_li(4)))

    def aside_requests(self):
        return ASIDE_REQUESTS(self.css_response(summary_li(5)))

    def csp(self):
        return is_success(TAKE_FIRST(self.response.css(summary_li(2))))

    def referrer_policy(self):
        return is_success(TAKE_FIRST(self.response.css(summary_li(3))))


def is_success(li: Selector):
    return 'success' in li.css('i').attrib['class']
