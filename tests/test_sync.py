import datetime

from _twitch import utils
from _twitch.queries import clip_info
from _twitch.sync import Sync


def test_sync_all():
    LOGINS = ["reckful", "twitchrivals", "forsen", "nmplol"]
    clip_info_data = clip_info("PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21")
    vod_interval = utils.clip_time(clip_info=clip_info_data)
    interval_times = Sync(logins=LOGINS).sync_all(vod_interval=vod_interval)

    assert "forsen" not in interval_times
    assert "nmplol" not in interval_times
    assert interval_times == {
        "twitchrivals": ("454052840", datetime.timedelta(seconds=28104)),
        "reckful": ("454177099", datetime.timedelta(seconds=10850)),
    }


def test_sync_all__clips(mocker):
    mocker.patch(
        "_twitch.clips.broadcaster_id_from_video_id",
        return_value={"video": {"owner": {"id": "1"}}},
    )
    mocker.patch(
        "_twitch.clips.create_clip_mutation",
        return_value={
            "createClip": {"clip": {"slug": "fake-clip-slug"}, "error": None},
        },
    )
    mocker.patch(
        "_twitch.clips.publish_clip_mutation",
        return_value={
            "publishClip": {"clip": {"slug": "fake-clip-slug"}, "error": None},
        },
    )

    LOGINS = ["reckful"]
    clip_info_data = clip_info("PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21")
    vod_interval = utils.clip_time(clip_info=clip_info_data)
    interval_times = Sync(logins=LOGINS).sync_all(
        vod_interval=vod_interval,
        clip_titles="tests",
    )

    assert interval_times == {"reckful": ("454177099", 10850.0, "fake-clip-slug")}
