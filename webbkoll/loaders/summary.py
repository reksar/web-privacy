from scrapy.selector import Selector
from webbkoll.items import SummaryItem
from .data_class import DataclassLoader
from .cookies import CookiesLoader
from .common import summary_li, find, take_first, html


IP = '.'.join(['\d{1,3}'] * 4)
# TODO: remove when the aside requests will be implemented as separated item.
COUNT = '\d.*'


# TODO: Callable loader class
class SummaryLoader(DataclassLoader):
    data_class = SummaryItem

    def __call__(self, response):
        self.update(response)
        self.populate()
        return self.load_item()

    def update(self, response):
        self.selector = Selector(response=response)
        self.context.update(selector=self.selector)
        self.context.update(response=response)

    def populate(self):
        self.add_value('summary_url', self.context['response'].url)
        self.add_value('cookies', self.context['response'], CookiesLoader())
        for args in (
            ('checked_url', '.url li:first-child a::text'),
            ('final_url', '.url li:last-child a::text'),
            ('ip', summary_li(6), find(IP)),
            ('default_https', summary_li(1), is_success),
            ('aside_requests', summary_li(5), find(COUNT)),
            ('csp', summary_li(2), is_success),
            ('referrer_policy', summary_li(3), is_success),
        ):
            self.add_css(*args)


@take_first
def is_success(li: str):
    return 'success' in html(li).css('i').attrib['class']
