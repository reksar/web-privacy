# Web privacy

Summary of web privacy, based on [webbkoll](https://webbkoll.dataskydd.net/en).

## Using

In common: pass an URL list in the `urls` arg to the `summary` spider

```bash
scrapy crawl summary -a urls="<URL_1 URL_2 ...>"
```

### Linux

Pass an URL list to the `run.sh`, e.g.:

```bash
run.sh `cat urls.txt`
```

### Windows

Just `run.bat`.

But you need to take care of using a Python **virtual environment**, 
installing the required Python packages and editing the `urls.txt` manually.

Use the `run.sh` as an example.

**Note:** remove `--nolog` to debug from runners.
