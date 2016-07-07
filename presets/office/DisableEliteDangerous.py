#!/usr/bin/python
import os, sys
import json

try:
    from iron_mq import *
except ImportError, ie:
    print "Please Install IronMQ Bindings for Python"
    print ""
    print "pip install iron-mq"
    print ""
    sys.exit(1)

class IronQueue:
    @staticmethod
    def get():
        project_token = '0NW3J3M4FljVVK2DoUzU5EwZIWk'
        project_id = '5681a0ce42887600090000dc'

        return IronMQ(
                host='mq-aws-eu-west-1-1.iron.io',
                project_id=project_id,
                token=project_token,
                protocol='https',
                port=443,
                api_version=3,
                config_file=None)

if __name__ == '__main__':
    broker = IronQueue.get()
    print "Queues: %s" % broker.queues()
    queue = broker.queue('lights-circadian')
    payload = {'room_id': 6, 'enabled':True}
    queue.post(json.dumps(payload))
