from operator import attrgetter as attr


def issues(infolist):
    return filter(attr('cookies'), infolist)
