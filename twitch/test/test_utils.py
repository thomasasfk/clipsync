import pytest
import twitch.src.utils as utils


def test_extractClipTime():
    clipInfo = {'clip': {'video': {'createdAt': '2017-09-12T17:36:46Z'}, 'videoOffsetSeconds': 5452}}
    clipTime = utils.clipTime(clipInfo=clipInfo)

    assert str(clipTime) == "2017-09-12 19:07:38"


@pytest.mark.parametrize('login, expected',
                         [('sodapoppin',          True),
                          ('trainwrecks_tv',      True),
                          ('Gav',                 True),
                          ('2020-11-27 23:52:26', False),
                          ('/invalid/',           False),
                          ('https://google.com',  False), ])
def test_validLogin(login, expected):
    validLogin = utils.validLoginFormat(login=login)

    if validLogin:
        assert validLogin.group(0) == login
    assert bool(validLogin) == expected


@pytest.mark.parametrize('seconds, expectedTimestamp',
                         [(3600,  '1h'),
                          (50,    '50s'),
                          (70,    '1m10s'),
                          (3661,  '1h1m1s'),
                          (3601,  '1h1s'),
                          (86400, '24h'),
                          (-1,    '-1s'),
                          (0,     '0s'), ])
def test_secondsToTimestamp(seconds, expectedTimestamp):
    timestamp = utils.secondsToTimestamp(seconds)

    assert timestamp == expectedTimestamp


@pytest.mark.parametrize('seconds, expectedTimestamp',
                         [(3600,  '1h0m0s'),
                          (50,    '0h0m50s'),
                          (70,    '0h1m10s'),
                          (3661,  '1h1m1s'),
                          (3601,  '1h0m1s'),
                          (86400, '24h0m0s'),
                          (-1,    '-0h0m1s'),
                          (0,     '0h0m0s'), ])
def test_secondsToTimestampWithZeros(seconds, expectedTimestamp):
    timestamp = utils.secondsToTimestamp(seconds, zeros=True)

    assert timestamp == expectedTimestamp


@pytest.mark.parametrize('timestamp, expectedSeconds',
                         [('1h1m1s', 3661),
                          ('1h1s',   3601),
                          ('1h1m',   3660),
                          ('1h',     3600),
                          ('1m1s',     61),
                          ('1m',       60),
                          ('0h0m0s',    0)])
def test_timestampToSeconds(timestamp, expectedSeconds):
    timestamp = utils.timestampToSeconds(timestamp)

    assert timestamp == expectedSeconds

