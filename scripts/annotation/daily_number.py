import datetime
import json
import sys
import time
import urllib2
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
HYPO_SEARCH_API = 'https://api.hypothes.is/search?limit=0'

# 60*60*24 (1day)
delay = 86400
if len(sys.argv) > 1:
    delay = int(sys.argv[1])

sock = socket()
try:
    sock.connect((CARBON_SERVER, CARBON_PORT))
except:
    print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?"\
          % {'server': CARBON_SERVER, 'port': CARBON_PORT}
    sys.exit(1)

while True:
    # Generate before and after time strings
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    query = "&before=%s&after=%s" % (tomorrow.isoformat(), today.isoformat())

    response = urllib2.urlopen(HYPO_SEARCH_API) # Add query to here
    data = json.load(response)

    timestamp = time.mktime(today.timetuple())
    lines = ["system.annotation_number_1day %d %d" % (data['total'], timestamp)]
    # all lines must end in a newline
    message = '\n'.join(lines) + '\n'
    print "sending message\n"
    print '-' * 80
    print message
    print
    sock.sendall(message)
    time.sleep(delay)
