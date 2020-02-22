url = 'http://smava.de'
import selenium.webdriver
ONLINE_CHECKER = 'https://webbkoll.dataskydd.net/en'
browser = selenium.webdriver.Chrome()
browser.get(ONLINE_CHECKER)
url_input = browser.find_element_by_css_selector('input[name="url"]')
url_input.send_keys(url)
url_input.submit()
results = browser.find_element_by_id('results-header')
summary = results.find_element_by_css_selector('.summary')
cookies = summary.find_element_by_css_selector('li:nth-child(4) > strong')
print(cookies.text)
browser.quit()
