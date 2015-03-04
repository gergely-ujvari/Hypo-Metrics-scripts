import datetime
import json
import urllib2

HYPO_SEARCH_API = 'https://api.hypothes.is/search'


def get_daily_data():
    annotations = []

    # Generate before and after time strings
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    offset = 0
    limit = 100
    total = 1

    while offset < total:
        query = '?offset=%d&limit=%d&before=%s&after=%s' % \
                (offset, limit, tomorrow.isoformat(), today.isoformat())
        request_uri = HYPO_SEARCH_API + query
        resp = urllib2.urlopen(request_uri)
        payload = json.load(resp)

        total = payload['total']
        fetched = len(payload['rows'])
        offset += fetched

        annotations.extend(payload['rows'])

    return annotations
