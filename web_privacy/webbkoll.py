import selenium.webdriver as Se
import info


class Webbkoll:

    url = 'https://webbkoll.dataskydd.net/en'
    selector = {
        'url_input': 'input[name="url"]',
        'result': '#results-summary',
        'given_url': '.url li:first-child > a',
        'url': '.url li:last-child > a',
        'cookies': '.summary li:nth-child(4) > strong',
    }

    def __init__(self):
        timeout_sec = 30
        self.browser = Se.Chrome()
        self.wait = Se.support.ui.WebDriverWait(self.browser, timeout_sec)

    def __del__(self):
        try:
            self.browser.quit()
        except ImportError:
            pass

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
        given_url = self.find('given_url')
        given_url = given_url.get_attribute('href')
        url = self.find('url')
        url = url.get_attribute('href')
        cookies = self.find('cookies')
        cookies = cookies.text
        cookies = int(cookies)
        return info.Info(given_url, url, cookies)
