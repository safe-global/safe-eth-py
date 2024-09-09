#!/bin/sh

# Execute mypy and stop script if it fails
mypy . || exit 1

# Postgresql and ganache-cli must be running for the tests
docker-compose up -d db ganache

sleep 3

# python manage.py test --settings=config.settings.test
DJANGO_SETTINGS_MODULE=config.settings.test pytest
docker-compose down
