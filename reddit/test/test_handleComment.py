import pickle
import datetime

from reddit.src.handleComment import handleComment

RECKFUL_TWITCH_RIVALS_INTERVAL_TIMES = {'twitchrivals': ('454052840', datetime.timedelta(seconds=28104)),
                                        'reckful': ('454177099', datetime.timedelta(seconds=10850))}


def setupComment():
    file = open("reddit/test/commentMock", 'rb')
    return pickle.load(file)


def test_handleComment():
    comment = setupComment()
    comment.body = "u/clipsynctest reckful twitchrivals forsen nmplol"
    comment.link_url = "https://clips.twitch.tv/PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21"
    intervalTimes = handleComment(comment, 'clipsynctest')
    assert 'forsen' not in intervalTimes
    assert 'nmplol' not in intervalTimes
    assert intervalTimes == RECKFUL_TWITCH_RIVALS_INTERVAL_TIMES

# todo:  tests are a mess and hitting all real endpoints, better differentiate unit/integration tests
