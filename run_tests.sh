#!/bin/sh
# Postgresql and anvil must be running for the tests

docker compose up -d --wait db anvil

# python manage.py test --settings=config.settings.test
DJANGO_SETTINGS_MODULE=config.settings.test pytest
docker compose down
