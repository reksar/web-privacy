from abc import ABC, abstractmethod
from dataclasses import fields
from operator import attrgetter as attr
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from itemloaders.processors import TakeFirst


class DataclassHelper(ABC):

    @property
    @abstractmethod
    def dataclass(self):
        # Should return one of the dataclasses described in `items.py`.
        pass

    @property
    def field_names(self):
        yield from map(attr('name'), fields(self.dataclass))


class DataclassLoader(ItemLoader, DataclassHelper):
    """
    Using the `ItemLoader` pollutes a dataclass declaration for a scrapy item.
    See: https://docs.scrapy.org/en/latest/topics/loaders.html#working-with-dataclass-items

    This loader allows to keep dataclasses pure and frozen.
    See `items.py`.

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

    def css_response(self, selector):
        """
        Instead of `ItemLoader.nested_css()` to pass nested response to
        loaders with a type other than the original.
        """
        match_list = self.selector.css(selector)
        first_match = match_list.get()
        return HtmlResponse('', body=first_match, encoding='utf-8')
