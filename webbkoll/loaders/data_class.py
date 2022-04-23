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

    # The `ItemLoader` uses a mutable dicts under the hood.
    default_item_class = dict

    # Override it to a dataclass item further.
    # TODO: make abstract
    data_class = dict

    def __call__(self, response):
        self.update(response)
        self.populate()  # TODO: make abstract
        return self.load_item()

    def update(self, response):
        self.selector = Selector(response=response)
        self.context.update(selector=self.selector)
        self.context.update(response=response)

    def load_item(self):
        return self.data_class(**super().load_item())
