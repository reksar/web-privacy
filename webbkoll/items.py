from scrapy import Item, Field


# TODO: add link to the summary web page
# TODO: split first- and third-party cookies
# TODO: split requests and hosts count
class SummaryItem(Item):
    checked_url = Field()
    final_url = Field()
    ip = Field()
    default_https = Field()
    cookies = Field()
    aside_requests = Field()
    csp = Field()
    referrer_policy = Field()
