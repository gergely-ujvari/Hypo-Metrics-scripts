import datetime
import json
import urllib2

import config


def get_daily_data(day):
    annotations = []

    # Generate before time string
    next_day = day + datetime.timedelta(days=1)

    offset = 0
    limit = 100
    total = 1
    fetched = 1

    while offset < total and fetched > 0:
        query = '?offset=%d&limit=%d&before=%s&after=%s' % \
                (offset, limit, next_day.isoformat(), day.isoformat())
        request_uri = config.config[config.HYPO_SEARCH_API] + query
        request = urllib2.Request(request_uri)
        request.add_header('X-Annotator-Auth-Token', config.config[config.HYPO_AUTH_TOKEN])
        resp = urllib2.urlopen(request)
        payload = json.load(resp)

        total = payload['total']
        fetched = len(payload['rows'])
        offset += fetched

        annotations.extend(payload['rows'])

    return annotations
