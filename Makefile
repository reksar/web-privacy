.DEFAULT_GOAL := run

.PHONY: run
run:
	scrapy crawl summary --nolog -o -:json
