from scrapy.http import HtmlResponse


def summary_li(nth):
    # CSS selector for `nth` <li> of the <div.summary> <ul>.
    return f".summary li:nth-child({nth})"


def html(body: str):
    return HtmlResponse(url='', body=body, encoding='utf-8')


def select_css(selector: callable):
    """
    Allows to return a CSS selector from `DataclassLoader` methods. Without
    using `replace_css()` instead of `replace_value()` during
    `DataclassLoader.populate()` in this case.
    """
    return lambda self: self._get_cssvalues(selector(self))
