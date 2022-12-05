from _twitch.queries import clip_info
from _twitch.queries import multi_user_vods_info
from _twitch.queries import user_vods_info


def test_ClipInfo_post():
    data = clip_info("TrappedFrigidPenguinSeemsGood")

    assert data == {
        "clip": {
            "video": {"id": "174256129", "createdAt": "2017-09-12T17:36:46Z"},
            "videoOffsetSeconds": 5452,
        },
    }


def test_MultiUserVodsInfo_post():
    data = multi_user_vods_info(logins=["xqc", "hasanabi"])

    assert len(data["users"]) == 2
    assert data["users"][0]["login"] == "xqc"
    assert data["users"][1]["login"] == "hasanabi"


def test_UserVodsInfo_post():
    data = user_vods_info(login="xqc")

    assert data["user"]["login"] == "xqc"
    assert len(data["user"]["videos"]["edges"]) > 0
