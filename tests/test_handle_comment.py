import pickle

import config
from _reddit.handle_comment import handle_comment
from _twitch.sync import Sync


def setup_comment():
    comment_mock = open("testing/comment_mock", "rb")
    return pickle.load(comment_mock)


def test_handle_comment(mocker):
    comment = setup_comment()
    mocker.patch.object(comment, "refresh", return_value=None)
    mocker.patch.object(comment, "reply", return_value=comment)
    mocker.patch.object(
        Sync,
        "sync_all",
        return_value={
            "twitchrivals": ("454052840", 28104.0, None),
            "reckful": ("454177099", 10850.0, None),
        },
    )
    mocker.patch.object(config.REDDIT, "USERNAME", "clipsynctest")

    comment.body = "u/clipsynctest reckful twitchrivals forsen nmplol"
    comment.link_url = (
        "https://clips.twitch.tv/PluckyCreativeAlpacaPicoMause-_o6_deF5l0ADBa21"
    )

    success_status, reply = handle_comment(comment)

    assert success_status == 0
    assert "Username | Vod" in reply
    assert "-------- | ----" in reply
    assert (
            "[twitchrivals](https://www.twitch.tv/twitchrivals/?) | [7h48m24s]("
            "https://www.twitch.tv/videos/454052840?t=7h48m24s)"
            in reply
    )
    assert (
            "[reckful](https://www.twitch.tv/reckful/?) | [3h0m50s](https://www.twitch.tv/videos/454177099?t=3h0m50s)"
            in reply
    )
    assert (
            "[watch via twitchmultivod](https://twitchmultivod.com/#/454177099?t=3h50s/454052840/454177099)"
            in reply
    )
    assert (
            "^(*This is an automated response* ) ^| ^[Feedback]("
            "http://www.reddit.com/message/compose/?to=wee_tommy&subject=Feedback:&message=%5BPost%5D\\("
            "https://reddit.com/comments/n46wjz//gwtuoq3/\\)) "
            in reply
    )

    comment.reply.assert_called_once_with(reply)
