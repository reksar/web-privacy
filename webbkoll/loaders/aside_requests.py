from webbkoll.items import AsideRequestsItem
from webbkoll.loaders.cookies import MATCH_GROUP
from .dataclass import DataclassLoader
from .common import summary_li, find


REQUESTS = '(\d+) requests'
HOSTS = '(\d+) unique hosts'
# For all of the above patterns
MATCH_GROUP = 1


# TODO:
class AsideRequestsLoader(DataclassLoader):
    """
    The `response` is expected to contain the 5th <li> of the Webbkoll summary
    <ul> whose inner HTML end with some like:
        <strong>{requests}</strong>
    or
        <strong>{requests}</strong> requests to {hosts} unique hosts
    """

    @property
    def dataclass(self):
        return AsideRequestsItem

    def requests(self):
        return 0

    def hosts(self):
        return 0
