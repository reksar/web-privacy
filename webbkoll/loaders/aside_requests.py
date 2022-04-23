from webbkoll.items import AsideRequestsItem
from webbkoll.loaders.cookies import MATCH_GROUP
from .data_class import DataclassLoader
from .common import summary_li, find


REQUESTS = '(\d+) requests'
HOSTS = '(\d+) unique hosts'
# For all of the above patterns
MATCH_GROUP = 1

# TODO: nested loader
# Selector for the 5th <li> tag that contains the line of format
# '<x> requests to <y> unique hosts',
# but polluted with other HTML tags.
li = summary_li(5)


# FIXME: parse Third-party requests: 0
class AsideRequestsLoader(DataclassLoader):
    data_class = AsideRequestsItem

    def populate(self):
        self.replace_css('requests', li, find(REQUESTS, MATCH_GROUP))
        self.replace_css('hosts', li, find(HOSTS, MATCH_GROUP))
