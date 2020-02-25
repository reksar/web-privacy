import webbkoll


def check(urls):
    checker = webbkoll.Webbkoll()
    return map(checker.check, urls)
