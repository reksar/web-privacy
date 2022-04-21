import re
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst
from scrapy.http import HtmlResponse


LF = '\n'
SPACE = ' '
MULTISPACE = '\s{2,}'
TAKE_FIRST = TakeFirst()


def summary_li(idx):
    return f".summary li:nth-child({idx})"

def take_first(f):
    return lambda values: f(TAKE_FIRST(values))

def find(pattern, group=0, default=''):

    @take_first
    def find_in(value: str):
        try:
            # TODO: sanitize anywhere else?
            line = sanitize(value)
            match = re.search(pattern, line)
            return match.group(group)

        except (AttributeError, IndexError):
            return default

    return find_in

def sanitize(value: str):
    txt = remove_tags(value)
    line = txt.replace(LF, SPACE)
    return re.sub(MULTISPACE, SPACE, line)

def html(value: str):
    return HtmlResponse('', body=value, encoding='utf-8')
