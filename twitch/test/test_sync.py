import datetime
import twitch.src.utils as utils

from twitch.src.queries import ClipInfo, BroadcasterIDFromVideoID, CreateClipMutation, PublishClipMutation
from twitch.src.sync import Sync


def test_syncAll():
    LOGINS = ['reckful', 'twitchrivals', 'forsen', 'nmplol']
    clipInfo = ClipInfo.post('PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21')
    vodInterval = utils.clipTime(clipInfo=clipInfo)
    intervalTimes = Sync(logins=LOGINS).syncAll(vodInterval=vodInterval)

    assert 'forsen' not in intervalTimes
    assert 'nmplol' not in intervalTimes
    assert intervalTimes == {'twitchrivals': ('454052840', datetime.timedelta(seconds=28104)),
                             'reckful': ('454177099', datetime.timedelta(seconds=10850))}


def test_syncAllClips(mocker):
    mocker.patch.object(BroadcasterIDFromVideoID, 'post', return_value={'video': {'owner': {'id': '1'}}})
    mocker.patch.object(CreateClipMutation, 'post', return_value=
        {'createClip': {'clip': {'slug': 'fake-clip-slug'}, 'error': None}})
    mocker.patch.object(PublishClipMutation, 'post', return_value=
        {'publishClip': {'clip': {'slug': 'fake-clip-slug'}, 'error': None}})

    LOGINS = ['reckful']
    clipInfo = ClipInfo.post('PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21')
    vodInterval = utils.clipTime(clipInfo=clipInfo)
    intervalTimes = Sync(logins=LOGINS).syncAll(vodInterval=vodInterval, clipTitles="test")

    assert intervalTimes == {'reckful': ('454177099', 10850.0, 'fake-clip-slug')}
