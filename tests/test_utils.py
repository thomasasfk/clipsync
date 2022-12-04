import pytest

from _twitch import utils


def test_clip_time():
    clipInfo = {
        "clip": {
            "video": {"createdAt": "2017-09-12T17:36:46Z"},
            "videoOffsetSeconds": 5452,
        },
    }
    clipTime = utils.clip_time(clip_info=clipInfo)

    assert str(clipTime) == "2017-09-12 19:07:38"


@pytest.mark.parametrize(
    "login, expected",
    [
        ("sodapoppin", True),
        ("trainwrecks_tv", True),
        ("Gav", True),
        ("2020-11-27 23:52:26", False),
        ("/invalid/", False),
        ("https://google.com", False),
    ],
)
def test_valid_login(login, expected):
    valid_login = utils.valid_login_format(login=login)

    if valid_login:
        assert valid_login.group(0) == login
    assert bool(valid_login) == expected


@pytest.mark.parametrize(
    "seconds, expected_timestamp",
    [
        (3600, "1h"),
        (50, "50s"),
        (70, "1m10s"),
        (3661, "1h1m1s"),
        (3601, "1h1s"),
        (86400, "24h"),
        (-1, "-1s"),
        (0, "0s"),
    ],
)
def seconds_to_timestamp(seconds, expected_timestamp):
    timestamp = utils.seconds_to_timestamp(seconds)

    assert timestamp == expected_timestamp


@pytest.mark.parametrize(
    "seconds, expected_timestamp",
    [
        (3600, "1h0m0s"),
        (50, "0h0m50s"),
        (70, "0h1m10s"),
        (3661, "1h1m1s"),
        (3601, "1h0m1s"),
        (86400, "24h0m0s"),
        (-1, "-0h0m1s"),
        (0, "0h0m0s"),
    ],
)
def test_seconds_to_timestamp_zeros(seconds, expected_timestamp):
    timestamp = utils.seconds_to_timestamp(seconds, zeros=True)

    assert timestamp == expected_timestamp


@pytest.mark.parametrize(
    "timestamp, expected_seconds",
    [
        ("1h1m1s", 3661),
        ("1h1s", 3601),
        ("1h1m", 3660),
        ("1h", 3600),
        ("1m1s", 61),
        ("1m", 60),
        ("0h0m0s", 0),
    ],
)
def test_timestamp_to_seconds(timestamp, expected_seconds):
    timestamp = utils.timestamp_to_seconds(timestamp)

    assert timestamp == expected_seconds
