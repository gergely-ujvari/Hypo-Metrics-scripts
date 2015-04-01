import json
import time
import urllib2

from carbon import send
import config

# 30 sec
delay = 30

while True:
    uri = config.config[config.HYPO_SEARCH_API] + '?limit=0'
    request = urllib2.Request(uri)
    request.add_header('X-Annotator-Auth-Token', config.config[config.HYPO_AUTH_TOKEN])
    response = urllib2.urlopen(request)
    data = json.load(response)

    timestamp = int(time.time())
    lines = ["daily.annotations.total %d %d" % (data['total'], timestamp)]
    send(lines)

    time.sleep(delay)
