import selenium.webdriver as Se


class Webbkoll:

    url = 'https://webbkoll.dataskydd.net/en'
    selector = {
        'url_input': 'input[name="url"]',
        'result': '#results-summary',
        'cookies': '.summary li:nth-child(4) > strong',
    }

    def __init__(self):
        timeout_sec = 30
        self.browser = Se.Chrome()
        self.wait = Se.support.ui.WebDriverWait(self.browser, timeout_sec)

    def __del__(self):
        self.browser.quit()

    def find(self, selector_name, dom=None):
        selector = Webbkoll.selector[selector_name]
        dom = dom or self.browser
        return dom.find_element_by_css_selector(selector)

    def check(self, url):
        self.get_start_page()
        self.analyze(url)
        return self.parse_result()

    def get_start_page(self):
        self.browser.get(Webbkoll.url)

    def analyze(self, url):
        url_input = self.find('url_input')
        url_input.send_keys(url)
        url_input.submit()
        self.wait.until(self.has_result)

    def has_result(self, browser):
        return self.find('result', browser)

    def parse_result(self):
        return self.find('cookies').text
