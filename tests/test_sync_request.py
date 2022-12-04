from _reddit.sync_request import TwitchClipSyncRequest
from _reddit.sync_request import TwitchVodSyncRequest
from _twitch.queries import ClipInfo
from _twitch.queries import VodCreatedAt

CLIP_INFO_RESPONSE = {
    "clip": {
        "video": {"id": "174256129", "createdAt": "2017-09-12T17:36:46Z"},
        "videoOffsetSeconds": 5452,
    },
}
VOD_CREATED_AT_RESPONSE = {"video": {"createdAt": "2017-09-12T17:36:46Z"}}


def test_TwitchClipSyncRequest_success(mocker):
    syncRequest = TwitchClipSyncRequest("TrappedFrigidPenguinSeemsGood")
    mocker.patch.object(ClipInfo, "post", return_value=CLIP_INFO_RESPONSE)
    result = syncRequest.retrieve_interval_time()
    assert str(result) == "2017-09-12 19:07:38"


def test_TwitchClipSyncRequest_failure(mocker):
    syncRequest = TwitchClipSyncRequest("TrappedFrigidPenguinSeemsGood")
    mocker.patch.object(ClipInfo, "post", return_value=None)
    result = syncRequest.retrieve_interval_time()
    assert result is None


def test_TwitchVodSyncRequest_success(mocker):
    mocker.patch.object(VodCreatedAt, "post", return_value=VOD_CREATED_AT_RESPONSE)
    syncRequest = TwitchVodSyncRequest("174256129", 5452)
    result = syncRequest.retrieve_interval_time()
    assert str(result) == "2017-09-12 19:07:38"


def test_TwitchVodSyncRequest_failure(mocker):
    mocker.patch.object(VodCreatedAt, "post", return_value=None)
    syncRequest = TwitchVodSyncRequest("174256129", 5452)
    result = syncRequest.retrieve_interval_time()
    assert result is None
