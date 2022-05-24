from abc import ABC, abstractmethod
from dataclasses import fields
from operator import attrgetter as attr
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from itemloaders.processors import TakeFirst
from .common import html


class DataclassHelper(ABC):

    @property
    @abstractmethod
    def dataclass(self):
        raise NotImplementedError("Sould return a dataclass from `items.py`")

    @property
    def field_names(self):
        yield from map(attr('name'), fields(self.dataclass))


class DataclassLoader(ItemLoader, DataclassHelper):
    """
    Using the `ItemLoader` pollutes a dataclass declaration for a scrapy item.
    See: https://docs.scrapy.org/en/latest/topics/loaders.html#working-with-dataclass-items

    This loader allows to keep dataclasses pure and frozen. See `items.py`.

    In subclasses, you must override the `dataclass()` abstract property and
    define all methods needed to `populate()` objects, see the method below.
    """

    default_output_processor = TakeFirst()

    # The `ItemLoader` uses mutable dict under the hood.
    default_item_class = dict

    @property
    def response(self):
        return self.context['response']

    def __call__(self, response):
        self.update(response)
        self.populate()
        return self.load_item()

    def update(self, response):
        self.selector = Selector(response=response)
        self.context.update(selector=self.selector)
        self.context.update(response=response)

    def populate(self):
        """
        For each `self.field_names` calls the `self.<field_name>()` method to
        get the field value and store it internally for loading the item
        further.

        NOTE: using `replace_value()` instead of `add_value()` keeps the first
        item of the internal list is actual. So using the `TakeFirst` as the
        `default_output_processor` works correctly.
        """
        for name in self.field_names:
            self.replace_value(name, getattr(self, name)())

    def load_item(self):
        return self.dataclass(**super().load_item())

    def css_response(self, query):
        """
        Builds a `HtmlResponse` from a HTML text selected with the CSS `query`
        from `self.response`.

        It allows to call a `DataclassLoader` with a nested response similar
        to `ItemLoader.nested_css()`, but without instantiating the current
        class.
        """
        return html(self.selector.css(query).get())
