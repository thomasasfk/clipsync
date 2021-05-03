from pytest_mock import mocker

from reddit.src.sync_request import TwitchClipSyncRequest
from twitch.src.queries import ClipInfo

CLIP_INFO_RESPONSE = {'clip': {'video': {'createdAt': '2017-09-12T17:36:46Z'}, 'videoOffsetSeconds': 5452}}

def test_TwitchClipSyncRequest(mocker):
    syncRequest = TwitchClipSyncRequest('TrappedFrigidPenguinSeemsGood')
    mocker.patch.object(ClipInfo, 'post', return_value=CLIP_INFO_RESPONSE)
    result = syncRequest.retrieveIntervalTime()
    assert str(result) == '2017-09-12 19:07:38'

