import pytest

from reddit.src.linkValidator import validateLink
from reddit.src.syncRequest import SyncRequest, InvalidSyncRequest

validLinks = [
    "https://clips.twitch.tv/DepressedEnchantingRabbitMrDestructoid",
    "https://m.twitch.tv/clip/BigSarcasticWalrusRlyTho",
    "https://twitch.tv/CLIP/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
    "https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=23397s",
    "https://www.twitch.tv/videos/992654496?sr=a&t=23397s",
    "https://m.twitch.tv/sykkuno/v/992654496?sr=a&t=23397s",
    "https://m.twitch.tv/VIDEOS/992654496?sr=a&t=23397s",
    "https://m.twitch.tv/videos/992654496?t=23397s&",
]

invalidLinks = [
    "https://clips.twitch.com/DepressedEnchantingRabbitMrDestructoid",
    "https://clips.twitch.tv/",
    "https://youtube.com/clip/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
    "https://twitch.tv/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
    "https://www.twitch.tv/videos/992654496",
    "https://m.twitch.tv/sykkuno/992654496?sr=a&t=23397s",
    "992654496?sr=a&t=23397s",
    ""
]


@pytest.mark.parametrize("link", validLinks)
def test_link_validator_valid(link):
    valid_link = validateLink(link)
    assert valid_link is not None
    assert isinstance(valid_link, SyncRequest)


@pytest.mark.parametrize("link", invalidLinks)
def test_link_validator_invalid(link):
    invalid_link = validateLink(link)
    assert isinstance(invalid_link, InvalidSyncRequest)

