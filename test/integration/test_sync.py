import datetime
import twitch.utils as utils

from twitch.queries import ClipInfoQuery
from twitch.sync import Sync


def test_syncAll():
    LOGINS = ['reckful', 'twitchrivals', 'forsen', 'nmplol']
    clipInfo = ClipInfoQuery.post('PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21')
    vodInterval = utils.clipTime(clipInfo=clipInfo)
    intervalTimes = Sync(logins=LOGINS).syncAll(vodInterval=vodInterval)

    assert 'forsen' not in intervalTimes
    assert 'nmplol' not in intervalTimes
    assert intervalTimes == {'twitchrivals': ('454052840', datetime.timedelta(seconds=28104)),
                             'reckful': ('454177099', datetime.timedelta(seconds=10850))}
