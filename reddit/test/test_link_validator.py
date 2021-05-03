import pytest

from reddit.src.link_validator import validate
from reddit.src.sync_request import SyncRequest

valid_links = [
    "https://clips.twitch.tv/DepressedEnchantingRabbitMrDestructoid",
    "https://m.twitch.tv/clip/BigSarcasticWalrusRlyTho",
    "https://twitch.tv/clip/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
    "https://www.twitch.tv/sykkuno/v/992654496?sr=a&t=23397s",
    "https://www.twitch.tv/videos/992654496?sr=a&t=23397s",
    "https://m.twitch.tv/sykkuno/v/992654496?sr=a&t=23397s",
    "https://m.twitch.tv/videos/992654496?sr=a&t=23397s",
    "https://m.twitch.tv/videos/992654496?t=23397s&",
]

invalid_links = [
    "https://clips.twitch.com/DepressedEnchantingRabbitMrDestructoid",
    "https://clips.twitch.tv/",
    "https://youtube.com/clip/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
    "https://twitch.tv/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
    "https://www.twitch.tv/videos/992654496",
    "https://m.twitch.tv/sykkuno/992654496?sr=a&t=23397s",
    "992654496?sr=a&t=23397s",
    ""
]


@pytest.mark.parametrize("link", valid_links)
def test_link_validator(link):
    valid_link = validate(link)
    assert valid_link is not None
    assert isinstance(object, SyncRequest)


@pytest.mark.parametrize("link", invalid_links)
def test_link_validator(link):
    valid_link = validate(link)
    assert valid_link is False

