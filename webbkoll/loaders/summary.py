from webbkoll.items import SummaryItem
from .data_class import DataclassLoader
from .cookies import CookiesLoader
from .aside_requests import AsideRequestsLoader
from .common import summary_li, find, take_first, html


IP = '.'.join(['\d{1,3}'] * 4)


class SummaryLoader(DataclassLoader):
    data_class = SummaryItem

    def populate(self):
        response = self.context['response']

        for args in (
            ('summary_url', response.url),
            ('cookies', response, CookiesLoader()),
            ('aside_requests', response, AsideRequestsLoader()),
        ):
            self.replace_value(*args)

        for args in (
            ('checked_url', '.url li:first-child a::text'),
            ('final_url', '.url li:last-child a::text'),
            ('ip', summary_li(6), find(IP)),
            ('default_https', summary_li(1), is_success),
            ('csp', summary_li(2), is_success),
            ('referrer_policy', summary_li(3), is_success),
        ):
            self.replace_css(*args)


@take_first
def is_success(li: str):
    return 'success' in html(li).css('i').attrib['class']
