import selenium.webdriver


class Webbkoll:

    URL = 'https://webbkoll.dataskydd.net/en'

    def __init__(self):
        self.browser = selenium.webdriver.Chrome()

    def __del__(self):
        self.browser.quit()

    def check(self, url):
        self.browser.get(Webbkoll.URL)
        url_input = self.browser.find_element_by_css_selector('input[name="url"]')
        url_input.send_keys(url)
        url_input.submit()
        # TODO: wait
        summary_header = self.browser.find_element_by_id('results-summary')
        cookies_summary = summary_header.find_element_by_css_selector('.summary li:nth-child(4) > strong')
        return cookies_summary.text
