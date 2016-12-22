#!/usr/bin/env python
import requests
import redis
from decouple import config,Csv
from StringIO import StringIO
# from retrying import retry

url_template = "https://{channel}.release.core-os.net" \
               "/amd64-usr/current/version.txt"

COREOS_CHANNELS=config('COREOS_CHANNELS',default='stable,beta,alpha',cast=Csv())
WEBHOOK_KEY=config('WEBHOOK_KEY',default='COREOS_VERSION')
WEBHOOK_URL=config('WEBHOOK_URL',default='')

REDIS_HOST=config("REDIS_HOST",default='redis')
REDIS_PORT=config("REDIS_PORT",default='6379')
r = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)

# @retry
def save(channel,dataset):
    try:
        r.hmset("coreos:{channel}".format(channel=channel),dataset)
        msg = "Saved data for current coreos {channel} release to " \
              "redis://{host}:{port}".format(
              channel=channel,host=REDIS_HOST,port=REDIS_PORT)
        print msg
    except redis.ConnectionError:
        msg = "Unable to connect to redis://{host}:{port}".format(
              host=REDIS_HOST,port=REDIS_PORT)
        print msg
        raise Exception(msg)

# @retry
def curl(channel):
    url = (url_template.format(channel=channel))
    q = requests.get(url)

    if q.status_code == 200:
        dataset = {}
        for line in StringIO(q.content).readlines():
            # parse lines into dictionary
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k,v = line.split('=',1)
            dataset[k]=v.strip()
        return dataset
    else:
        msg = "GET {url} return status_code:{status_code}".format(
                url=url,status_code=q.status_code)
        raise Exception(msg)

def test_and_trigger(channel,new,key,url):
    old=r.hgetall("coreos:{channel}".format(channel=channel))
    if old == {} or (old[key] != new[key]):
        print "coreos:{channel} - {key} change detected, calling: {webhook}" \
              .format(channel=channel,key=key,webhook=url)
        data={"channel":channel,"old":old,"new":new}
        p = requests.post(url,json=data)
        print "POST {url} returned status_code: {status_code}".format(
                url=url,status_code=p.status_code)
    else:
        print "no change in {channel} release channel".format(channel=channel)

for channel in COREOS_CHANNELS:
    # get current release for channel
    current=curl(channel)
    if WEBHOOK_URL != '':
        test_and_trigger(channel,current,WEBHOOK_KEY,WEBHOOK_URL)
    save(channel,current)
