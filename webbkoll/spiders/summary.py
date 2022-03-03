from scrapy import Spider, FormRequest


class SummarySpider(Spider):
    name = 'summary'
    start_urls = ['https://webbkoll.dataskydd.net/']

    def parse(self, response):
        return FormRequest.from_response(
            response,
            formdata={
                'url': 'http://smava.de',
            },
            callback=summary)


def summary(response):
    return {
        'Checked URL': checked_url(response),
        'Final URL': final_url(response),
        'IP': ip(response),
        'HTTPS by default': has_https(response),
        'Cookies': cookies(response),
        'Third-party requests': third_party_requests(response),
        'Content Security Policy (CSP)': csp(response),
        'Referrer Policy': referrer_policy(response),
    }

def checked_url(response):
    return response.css('.url li:first-child a::text').get()

def final_url(response):
    return response.css('.url li:last-child a::text').get()

def ip(response):
    # TODO:
    pass

def has_https(response):
    return 'success' in response \
        .css('.summary li:first-child i') \
        .attrib['class']

def cookies(response):
    # TODO:
    pass

def third_party_requests(response):
    # TODO:
    pass

def csp(response):
    return 'success' in response \
        .css('.summary li:nth-child(2) i') \
        .attrib['class']

def referrer_policy(response):
    return 'success' in response \
        .css('.summary li:nth-child(3) i') \
        .attrib['class']
