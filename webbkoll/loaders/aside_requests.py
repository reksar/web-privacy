from w3lib.html import remove_tags
from webbkoll.items import AsideRequests
from .dataclass import DataclassLoader


"""
The `response` is expected to contain the 5th <li> of the Webbkoll summary <ul>
whose inner HTML end with some like:
    <strong>{requests}</strong>
or
    <strong>{requests}</strong> requests to {hosts} unique hosts
"""
REQUESTS = '<strong>\d+</strong>'
HOSTS = '(\d+) unique host'


class AsideRequestsLoader(DataclassLoader):

    @property
    def dataclass(self):
        return AsideRequests

    def requests(self):
        # TODO: cache
        return int(remove_tags(self.selector.re_first(REQUESTS)))

    def hosts(self):
        return int(self.selector.re_first(HOSTS)) if self.requests() else 0
