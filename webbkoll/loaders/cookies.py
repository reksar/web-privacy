from webbkoll.items import CookiesItem
from .dataclass import DataclassLoader
from .common import find


# First number in the parentheses
FIRST_PARTY = '\((\d+)'
# Number after the ';'
THIRD_PARTY = ';\s*(\d+)'
# Number before the parentheses
TOTAL = '(\d+)\s*\('
# For all of the above patterns
MATCH_GROUP = 1


# TODO:
class CookiesLoader(DataclassLoader):
    """
    The `response` is expected to contain the 4th <li> of the Webbkoll summary
    <ul> whose inner HTML end with some like:
        <strong>{total}</strong>
    or
        <strong>{total}</strong> ({x} first-party; {y} third-party)
    """

    @property
    def dataclass(self):
        return CookiesItem

    def total(self):
        return 0

    def first_party(self):
        return 0

    def third_party(self):
        return 0
