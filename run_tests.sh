#!/bin/sh
# Postgresql and ganache-cli must be running for the tests

docker ps | grep '\->5432' > /dev/null
if [ $? -eq 1 ]; then
    docker-compose up -d db
    sleep 3
    DATABASE_UP=1
else
    DATABASE_UP=0
fi

docker ps | grep '\->8545' > /dev/null
if [ $? -eq 1 ]; then
    docker-compose up -d ganache
    sleep 3
    GANACHE_UP=1
else
    GANACHE_UP=0
fi


# python manage.py test --settings=config.settings.test
DJANGO_SETTINGS_MODULE=config.settings.test pytest

if [ $DATABASE_UP -eq 1 ] || [ $GANACHE_UP -eq 1 ]; then
    docker-compose down
fi
