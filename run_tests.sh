#!/bin/sh
# Postgresql and ganache-cli must be running for the tests

ps aux | grep ganache-cli | grep -v grep > /dev/null
if [ $? -eq 1 ]; then
    echo 'Running Ganache-Cli'
    ganache-cli --defaultBalanceEther 10000 --gasLimit 10000000 -a 30 --chain.chainId 1337 --chain.networkId 1337 -d > /dev/null &
    GANACHE_PID=$!
    sleep 3
fi

docker ps | grep '\->5432' > /dev/null
if [ $? -eq 1 ]; then
    docker-compose up -d db
    sleep 3
    DATABASE_UP=1
else
    DATABASE_UP=0
fi


# python manage.py test --settings=config.settings.test
DJANGO_SETTINGS_MODULE=config.settings.test pytest

if [ ${GANACHE_PID:-0} -gt 1 ]; then
    echo 'Killing opened Ganache-Cli'
    kill $GANACHE_PID
fi

if [ $DATABASE_UP -eq 1 ]; then
    docker-compose down
fi
