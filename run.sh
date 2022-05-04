#!/bin/bash

readonly VENV=venv

venv_init() {
  if [ ! -d $VENV ]
  then
    python -m venv $VENV
  fi
}

venv_activate() {
  if [ -z $VIRTUAL_ENV ]
  then
    venv_init
    local readonly VENV_ACTIVATE=". $VENV/bin/activate"
    echo WARN: use $VENV_ACTIVATE
    $VENV_ACTIVATE
  fi
}

install() {
  export CRYPTOGRAPHY_DONT_BUILD_RUST=1
  pip install --upgrade pip
  pip install -r requirements.txt
}


venv_activate

if ! which scrapy > /dev/null
then
  install
fi

scrapy crawl summary --nolog -o -:json -a urls="$*"
