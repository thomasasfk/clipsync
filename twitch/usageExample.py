# I DONT KNOW HOW TO PACKAGE MANAGE IN PYTHON
from twitch.src.queries import ClipInfo
import twitch.src.utils as utils
from twitch.src.sync import Sync

clipInfo = ClipInfo.post('BreakableMushyKoupreyFutureMan-sO65-B7LjmditMWD')
vodInterval = utils.clipTime(clipInfo)

newSync = Sync(['esfandtv', 'penta', 'ratedepicz', 'kiwo', 'lunaoni'])
results = newSync.syncAll(vodInterval, "test")

for username, result in results.items():
    print(result)