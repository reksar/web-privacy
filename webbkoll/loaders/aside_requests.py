from scrapy.selector import Selector
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


# TODO: Callable loader class
class AsideRequestsLoader(DataclassLoader):
    data_class = AsideRequestsItem

    def __call__(self, response):
        self.update(response)
        self.populate()
        return self.load_item()

    def update(self, response):
        self.selector = Selector(response=response)
        self.context.update(selector=self.selector)
        self.context.update(response=response)

    def populate(self):
        self.add_css('requests', li, find(REQUESTS, MATCH_GROUP))
        self.add_css('hosts', li, find(HOSTS, MATCH_GROUP))
