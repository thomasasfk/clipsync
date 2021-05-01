import datetime

import pytest
import twitch.utils as utils
from twitch.queries import ClipInfo

from twitch.user import User


@pytest.mark.parametrize('login, expected',
                         [('reckful',      ('454177099', datetime.timedelta(seconds=10850))),
                          ('twitchrivals', ('454052840', datetime.timedelta(seconds=28104)))])
def test_Sync(login, expected):
    clipInfo = ClipInfo.post('PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21')
    clipTime = utils.clipTime(clipInfo=clipInfo)
    intervalTime = User(login).sync(clipTime)

    assert intervalTime == expected

def test_veryStart():
    clipTime = utils.parseTime('2010-11-27T21:06:12Z')
    intervalTime = User('xqcow').sync(clipTime)

    assert intervalTime == None

def test_paginate():
    user = User('reckful')
    assert len(user.edges) == 100
    user.paginate()
    assert len(user.edges) == 200
    user.paginate()
    assert len(user.edges) >= 201