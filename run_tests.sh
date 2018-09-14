#!/bin/sh
ps aux | grep ganache-cli | grep -v grep > /dev/null
if [ $? -eq 1 ]; then
    echo 'Running Ganache-Cli'
    ganache-cli -d --defaultBalanceEther 10000 -a 10 --noVMErrorsOnRPCResponse > /dev/null &
    GANACHE_PID=$!
    sleep 3
fi

python manage.py test --settings=config.settings.test

if [ ${GANACHE_PID:-0} -gt 1 ]; then
    echo 'Killing opened Ganache-Cli'
    kill $GANACHE_PID
fi
