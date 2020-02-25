import privacy


urls = (
    'https://webbkoll.dataskydd.net/en',
    'http://smava.de',
    'https://www.artstation.com/jakubrozalski',
    'https://yahoo.com',
)

info = privacy.check(urls)
print(info)
