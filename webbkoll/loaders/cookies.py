from scrapy.selector import Selector
from webbkoll.items import CookiesItem
from .data_class import DataclassLoader
from .common import summary_li, find


# First number in the parentheses
FIRST_PARTY = '\((\d+)'
# Number after the ';'
THIRD_PARTY = ';\s*(\d+)'
# Number before the parentheses
TOTAL = '(\d+)\s*\('
# For all of the above patterns
MATCH_GROUP = 1


# TODO: Callable loader class
class CookiesLoader(DataclassLoader):
    data_class = CookiesItem

    def __call__(self, response):
        self.update(response)
        self.populate()
        return self.load_item()

    def update(self, response):
        self.selector = Selector(response=response)
        self.context.update(selector=self.selector)
        self.context.update(response=response)

    def populate(self):

        # Selector for the 4th <li> tag that contains the line of format
        # '<total> (<x> first-party; <y> third-party)',
        # but polluted with other HTML tags.
        li = summary_li(4)

        self.add_css('first_party', li, find(FIRST_PARTY, MATCH_GROUP))
        self.add_css('third_party', li, find(THIRD_PARTY, MATCH_GROUP))
        self.add_css('total', li, find(TOTAL, MATCH_GROUP))
