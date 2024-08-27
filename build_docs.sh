#!/bin/sh

export DJANGO_SETTINGS_MODULE=config.settings.test
export DJANGO_DOT_ENV_FILE=.env.test
sphinx-apidoc -o docs/source/ safe_eth/
rm docs/source/*test*.rst
make -C docs/ clean
make -C docs/ html
