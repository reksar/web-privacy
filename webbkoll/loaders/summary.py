import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from itemloaders.processors import TakeFirst
from w3lib.html import remove_tags

from .data_class import DataclassLoader
from webbkoll.items import SummaryItem


LF = '\n'
SPACE = ' '
MULTISPACE = '\s{2,}'
IP = '.'.join(['\d{1,3}'] * 4)
COUNT = '\d.*'


class SummaryLoader(DataclassLoader):
    data_class = SummaryItem
    default_output_processor = TakeFirst()

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
        for args in (
            ('checked_url', '.url li:first-child a::text'),
            ('final_url', '.url li:last-child a::text'),
            ('ip', summary_li(6), find(IP)),
            ('default_https', summary_li(1), is_success),
            ('cookies', summary_li(4), find(COUNT)),
            ('aside_requests', summary_li(5), find(COUNT)),
            ('csp', summary_li(2), is_success),
            ('referrer_policy', summary_li(3), is_success),
        ):
            self.add_css(*args)


def summary_li(idx):
    return f".summary li:nth-child({idx})"

def take_first(f):
    return lambda values: f(SummaryLoader.default_output_processor(values))

def find(pattern):

    @take_first
    def find_in(value: str):
        line = sanitize(value)
        match = re.search(pattern, line)
        return match.group(0) if match else ''

    return find_in

@take_first
def is_success(value: str):
    return 'success' in html(value).css('i').attrib['class']

def html(value: str):
    return HtmlResponse('', body=value, encoding='utf-8')

def sanitize(value: str):
    txt = remove_tags(value)
    line = txt.replace(LF, SPACE)
    return re.sub(MULTISPACE, SPACE, line)
