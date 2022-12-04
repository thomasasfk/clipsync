from _twitch.queries import ClipInfo
from _twitch.queries import MultiUserVodsInfo
from _twitch.queries import UserVodsInfo


def test_ClipInfo_post():
    data = ClipInfo.post("TrappedFrigidPenguinSeemsGood")

    assert data == {
        "clip": {
            "video": {"id": "174256129", "createdAt": "2017-09-12T17:36:46Z"},
            "videoOffsetSeconds": 5452,
        },
    }


def test_MultiUserVodsInfo_post():
    data = MultiUserVodsInfo.post(logins=["xqc", "hasanabi"])

    assert len(data["users"]) == 2
    assert data["users"][0]["login"] == "xqc"
    assert data["users"][1]["login"] == "hasanabi"


def test_UserVodsInfo_post():
    data = UserVodsInfo.post(login="xqc")

    assert data["user"]["login"] == "xqc"
    assert len(data["user"]["videos"]["edges"]) > 0
