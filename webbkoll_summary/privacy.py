import webbkoll


def check(urls):
    checker = webbkoll.Webbkoll()
    return tuple(map(checker.check, urls))
