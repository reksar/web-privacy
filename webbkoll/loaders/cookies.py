from w3lib.html import remove_tags
from webbkoll.items import Cookies
from .dataclass import DataclassLoader


"""
The `response` is expected to contain the 4th <li> of the Webbkoll summary <ul>
whose inner HTML end with some like:
    <strong>{total}</strong>
or
    <strong>{total}</strong> ({x} first-party; {y} third-party)
"""
TOTAL = '<strong>\d+</strong>'
# The'(' followed by a number.
FIRST_PARTY = '\((\d+)'
# The '; ' followed by a number.
THIRD_PARTY = ';\s*(\d+)'


class CookiesLoader(DataclassLoader):

    @property
    def dataclass(self):
        return Cookies

    def total(self):
        # TODO: cache
        return int(remove_tags(self.selector.re_first(TOTAL)))

    def first_party(self):
        return int(self.selector.re_first(FIRST_PARTY)) if self.total() else 0

    def third_party(self):
        return int(self.selector.re_first(THIRD_PARTY)) if self.total() else 0
