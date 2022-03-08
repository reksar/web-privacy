from scrapy.loader import ItemLoader


class DataclassLoader(ItemLoader):
    """
    Using the `ItemLoader` pollutes the item data class declaration.
    See: https://docs.scrapy.org/en/latest/topics/loaders.html#working-with-dataclass-items

    This loader allows to keep dataclasses pure and frozen.
    See `items.py`.
    """

    # The `ItemLoader` uses a mutable dicts under the hood.
    default_item_class = dict

    # Reassign it to a dataclass item further.
    data_class = dict

    def load_item(self):
        return self.data_class(**super().load_item())
