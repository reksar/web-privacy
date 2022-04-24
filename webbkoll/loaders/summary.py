from webbkoll.items import SummaryItem
from .dataclass import DataclassLoader, select_css
from .cookies import CookiesLoader
from .aside_requests import AsideRequestsLoader
from .common import summary_li, find, TAKE_FIRST


IP = '.'.join(['\d{1,3}'] * 4)
SCRAP_COOKIES = CookiesLoader()
SCRAP_ASIDE_REQUESTS = AsideRequestsLoader()


class SummaryLoader(DataclassLoader):

    dataclass = SummaryItem

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
        return 0
        # TODO:
        return SCRAP_COOKIES(self.response)

    def aside_requests(self):
        return 0
        # TODO:
        return SCRAP_ASIDE_REQUESTS(self.response)

    def csp(self):
        return is_success(TAKE_FIRST(self.response.css(summary_li(2))))

    def referrer_policy(self):
        return is_success(TAKE_FIRST(self.response.css(summary_li(3))))


def is_success(li):
    return 'success' in li.css('i').attrib['class']
