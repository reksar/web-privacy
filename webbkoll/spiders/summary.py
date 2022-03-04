import re
from scrapy import Spider, FormRequest
from w3lib.html import remove_tags


class SummarySpider(Spider):
    name = 'summary'
    start_urls = ['https://webbkoll.dataskydd.net/']

    def parse(self, response):
        return FormRequest.from_response(
            response,
            callback=summary,
            formdata={
                'url': 'http://smava.de',
            }
        )


def summary(response):
    return {
        'Checked URL': checked_url(response),
        'Final URL': final_url(response),
        'IP': ip(response),
        'HTTPS by default': check_success(response, 1),
        'Cookies': cookies(response),
        'Third-party requests': third_party_requests(response),
        'Content Security Policy (CSP)': check_success(response, 2),
        'Referrer Policy': check_success(response, 3),
    }


def checked_url(response):
    return response.css('.url li:first-child a::text').get()

def final_url(response):
    return response.css('.url li:last-child a::text').get()

def cookies(response):
    cookies_re = '\d.*'
    cookies_txt = summary_li(response, 4).get()
    return find_line(cookies_re, cookies_txt)

def third_party_requests(response):
    requests_re = '\d.*'
    requests_txt = summary_li(response, 5).get()
    return find_line(requests_re, requests_txt)

def ip(response):
    ip_re = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ip_txt = summary_li(response, 6).get()
    return find_line(ip_re, ip_txt)

def check_success(response, li_idx):
    return 'success' in summary_li(response, li_idx).css('i').attrib['class']

def summary_li(response, li_idx):
    return response.css(f".summary li:nth-child({li_idx})")

def normalize_txt(txt):
    space = ' '
    multispace = '\s{2,}'
    oneline = txt.replace('\n', space)
    return re.sub(multispace, space, oneline)

def find_line(line_re, txt):
    oneline = normalize_txt(remove_tags(txt))
    match = re.search(line_re, oneline)
    return match.group(0) if match else ''
