.DEFAULT_GOAL := run
VENV_ACTIVATE := . venv/bin/activate

# This function combined with `.ONESHELL` targets allows a variables from
# Python virtual environment inside the recipes.
# Note: supressing a command output works for entire `.ONESHELL` recipe.
define venv_activate =
  if [ -z $$VIRTUAL_ENV ]
  then
    echo WARN: use \'$(VENV_ACTIVATE)\'
    $(VENV_ACTIVATE)
  fi
endef

.PHONY: run
.ONESHELL:
run: venv
	@$(call venv_activate)
	scrapy crawl summary --nolog -o -:json

.PHONY: install
.ONESHELL:
install: venv
	@$(call venv_activate)
	pip install --upgrade pip
	pip install -r requirements.txt

venv:
	# Python versioning with pyenv is recommended.
	python -m venv venv
