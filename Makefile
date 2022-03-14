.DEFAULT_GOAL := run

define venv_activate =
  if [ -z $$VIRTUAL_ENV ]; then . venv/bin/activate; fi
endef

.PHONY: run
.ONESHELL:
run: venv
	$(call venv_activate)
	scrapy crawl summary --nolog -o -:json

.PHONY: install
.ONESHELL:
install: venv
	$(call venv_activate)
	pip install --upgrade pip
	pip install -r requirements.txt

venv:
	# Python versioning with pyenv is recommended.
	python -m venv venv
