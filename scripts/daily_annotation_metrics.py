from collections import defaultdict
import time

from carbon import send
from daily_annotations import get_daily_data

# 60*60*24 (1day)
delay = 86400


def daily_annotation_total(annotations, timestamp):
    return ['daily.annotations.new %d %d' % (len(annotations), timestamp)]


def daily_uris(annotations, timestamp):
    uris = defaultdict(int)
    metrics = []

    for annotation in annotations:
        uri = annotation['uri']
        uris[uri] += 1

    for uri, total in uris.iteritems():
        metrics.append('daily.uri.%s %d %d' %
                       (uri, total, timestamp))

    metrics.append("daily.uris.total %d %d" %
                   (len(uris.keys()), timestamp))

    return metrics


def daily_users(annotations, timestamp):
    users = defaultdict(int)
    metrics = []

    for annotation in annotations:
        user = annotation['user']
        users[user] += 1

    for user, total in users.iteritems():
        username = user.split('acct:')[1]
        metrics.append('daily.user.%s %d %d' %
                       (username, total, timestamp))

    metrics.append('daily.user.total %d %d' %
                   (len(users.keys()), timestamp))

    return metrics

while True:
    lines = []
    timestamp = int(time.time())

    annotations = get_daily_data()

    lines.extend(daily_annotation_total(annotations, timestamp))
    lines.extend(daily_uris(annotations, timestamp))
    lines.extend(daily_users(annotations, timestamp))

    send(lines)
    time.sleep(delay)

