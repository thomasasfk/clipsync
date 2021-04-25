# I DONT KNOW HOW TO PACKAGE MANAGE IN PYTHON
from twitch.queries import ClipInfoQuery
import twitch.utils as utils
from twitch.sync import Sync

clipInfo = ClipInfoQuery.do_post('NaiveEntertainingDotterelRuleFive')
vodInterval = utils.clipTime(clipInfo)

newSync = Sync(['xqcow', 'hasanabi', 'tfue'])
results = newSync.syncAll(vodInterval)

for username, result in results.items():
    vodId = result[0]
    seconds = result[1].total_seconds()
    timestamp = utils.secondsToTimestamp(seconds)

    print(f'{username}: https://twitch.tv/videos/{vodId}?t={timestamp}')