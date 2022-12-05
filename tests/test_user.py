import datetime

import pytest

from _twitch import utils as utils
from _twitch.queries import clip_info
from _twitch.user import User


@pytest.mark.parametrize(
    "login, expected",
    [
        ("reckful", ("454177099", datetime.timedelta(seconds=10850))),
        ("twitchrivals", ("454052840", datetime.timedelta(seconds=28104))),
    ],
)
def test_Sync(login, expected):
    clip_info_data = clip_info("PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21")
    clip_time = utils.clip_time(clip_info=clip_info_data)
    interval_time = User(login).sync(clip_time)

    assert interval_time == expected


def test_veryStart():
    clip_time = utils.parse_time("2010-11-27T21:06:12Z")
    interval_time = User("xqc").sync(clip_time)

    assert interval_time is None


def test_paginate():
    user = User("reckful")
    assert len(user.edges) == 100
    user.paginate()
    assert len(user.edges) == 200
    user.paginate()
    assert len(user.edges) >= 201
