from dataclasses import fields
from operator import attrgetter as attr
from functools import wraps
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from itemloaders.processors import TakeFirst


# TODO: make abstract
class DataclassLoader(ItemLoader):
    """
    Using the `ItemLoader` pollutes the dataclass declaration for items.
    See: https://docs.scrapy.org/en/latest/topics/loaders.html#working-with-dataclass-items

    This loader allows to keep dataclasses pure and frozen.
    See `items.py`.
    """

    default_output_processor = TakeFirst()

    # The `ItemLoader` uses a mutable dict under the hood.
    default_item_class = dict

    # Override it to a dataclass item further.
    # TODO: make abstract
    dataclass = dict

    @property
    def response(self):
        return self.context['response']

    @property
    def field_names(self):
        yield from map(attr('name'), fields(self.dataclass))

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
        For each self.<dataclass>.<field_name> calls the self.<field_name>()
        method to get the field value and store it internally.

        Use the `replace_value()` not the `add_value()` to the internal list.
        """
        for name in self.field_names:
            get_value = getattr(self, name)
            value = get_value()
            self.replace_value(name, value)

    def load_item(self):
        return self.dataclass(**super().load_item())


def select_css(get_css_selector):
    # Selects value with CSS selector returned from the `loader_method`.

    @wraps(get_css_selector)
    def select(self):
        selector = get_css_selector(self)
        return self._get_cssvalues(selector)

    return select
