from webbkoll.items import CookiesItem
from .dataclass import DataclassLoader
from .common import summary_li, find


# First number in the parentheses
FIRST_PARTY = '\((\d+)'
# Number after the ';'
THIRD_PARTY = ';\s*(\d+)'
# Number before the parentheses
TOTAL = '(\d+)\s*\('
# For all of the above patterns
MATCH_GROUP = 1

# TODO: nested loader
# Selector for the 4th <li> tag that contains the line of format
# '<total> (<x> first-party; <y> third-party)',
# but polluted with other HTML tags.
li = summary_li(4)


# FIXME: parse Cookies: 0
class CookiesLoader(DataclassLoader):

    data_class = CookiesItem

    def populate(self):
        self.replace_css('first_party', li, find(FIRST_PARTY, MATCH_GROUP))
        self.replace_css('third_party', li, find(THIRD_PARTY, MATCH_GROUP))
        self.replace_css('total', li, find(TOTAL, MATCH_GROUP))

    def total(self):
        return find(self.response)
