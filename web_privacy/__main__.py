import sys
import privacy
import report


def filename():
    if len(sys.argv) > 1:
        return sys.argv[1]
    default = 'urls.txt'
    print(f'URLs file is not specified, trying to read {default} at root')
    return default


def read_urls():
    with open(filename()) as txt:
        return txt.read().split()


urls = read_urls()
infolist = privacy.check(urls)
issues = report.issues(infolist)
for issue in issues:
    print(issue.url, issue.cookies)
