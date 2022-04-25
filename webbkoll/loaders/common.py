import re
from functools import wraps
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst
from scrapy.selector import Selector


LF = '\n'
SPACE = ' '
MULTISPACE = '\s{2,}'
TAKE_FIRST = TakeFirst()


def summary_li(nth):
    """
    Returns the CSS selector for `nth` <li> of the <div.summary> <ul>.
    """
    return f".summary li:nth-child({nth})"

def take_first(f):
    """
    Decorator for function `f` that takes the first non-empty value `x` from
    iterable `values` and calls `f(x)` when `f(values)` is called externally.
    """
    return lambda values: f(TAKE_FIRST(values))

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

def select_css(get_css_selector):
    # Selects value with CSS selector returned from the `loader_method`.

    @wraps(get_css_selector)
    def select(self):
        selector = get_css_selector(self)
        return self._get_cssvalues(selector)

    return select
