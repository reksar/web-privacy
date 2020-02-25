import privacy
import report


urls = (
    'https://webbkoll.dataskydd.net/en',
    'http://smava.de',
    'https://www.artstation.com/jakubrozalski',
    'https://yahoo.com',
)

infolist = privacy.check(urls)
issues = report.issues(infolist)
for issue in issues:
    print(issue.url, issue.cookies)
