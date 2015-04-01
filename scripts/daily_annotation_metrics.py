import base64
from collections import defaultdict
import datetime
import time

from carbon import send
from daily_annotations import get_daily_data

# 30 sec
delay = 30
yesterday = None
yesterday_stamp = 0


def daily_annotation_new(annotations, timestamp):
    return ['daily.annotations.new %d %d' % (len(annotations), timestamp)]


def daily_uris(annotations, timestamp):
    uris = defaultdict(int)
    metrics = []

    for annotation in annotations:
        uri = annotation['uri']
        uris[uri] += 1

    for uri, total in uris.iteritems():
        encoded = base64.b64encode(uri)
        metrics.append('daily.uri.%s %d %d' %
                       (encoded, total, timestamp))

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

    today = datetime.date.today()
    if not yesterday:
        yesterday = today

    if today != yesterday:
        annotations = get_daily_data(yesterday)
        lines.extend(daily_annotation_new(annotations, yesterday_stamp))
        lines.extend(daily_uris(annotations, yesterday_stamp))
        lines.extend(daily_users(annotations, yesterday_stamp))

        yesterday = today
        yesterday_stamp = timestamp

    annotations = get_daily_data(today)

    lines.extend(daily_annotation_new(annotations, timestamp))
    lines.extend(daily_uris(annotations, timestamp))
    lines.extend(daily_users(annotations, timestamp))

    send(lines)

    time.sleep(delay)


