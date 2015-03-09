import json
import sys
import time
import urllib2

from carbon import send

HYPO_SEARCH_API = 'https://api.hypothes.is/search?limit=0'

# 60*60*24 (1day)
delay = 86400

while True:
    response = urllib2.urlopen(HYPO_SEARCH_API)
    data = json.load(response)

    timestamp = int(time.time())
    lines = ["daily.annotations.total %d %d" % (data['total'], timestamp)]
    send(lines)

    time.sleep(delay)
