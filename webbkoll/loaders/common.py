import re
from w3lib.html import remove_tags
from scrapy.http import HtmlResponse
from scrapy.selector import Selector


LF = '\n'
SPACE = ' '
MULTISPACE = '\s{2,}'


def summary_li(nth):
    # CSS selector for `nth` <li> of the <div.summary> <ul>.
    return f".summary li:nth-child({nth})"

def html(body: str):
    return HtmlResponse(url='', body=body, encoding='utf-8')

def find(pattern, html: Selector, group=0, default=''):
    try:
        # TODO: maybe use the `re_first()`?
        value = html.get()
        line = sanitize(value)
        match = re.search(pattern, line)
        return match.group(group)
    except (AttributeError, IndexError):
        return default

def sanitize(html: str):
    txt = remove_tags(html)
    line = txt.replace(LF, SPACE)
    return re.sub(MULTISPACE, SPACE, line)

def select_css(selector: callable):
    """
    Allows to return a CSS selector from `DataclassLoader` methods. Without
    using `replace_css()` instead of `replace_value()` during
    `DataclassLoader.populate()` in this case.
    """
    return lambda self: self._get_cssvalues(selector(self))
