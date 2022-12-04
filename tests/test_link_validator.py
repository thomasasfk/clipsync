import pytest

from _reddit.link_validator import validate_link
from _reddit.sync_request import InvalidSyncRequest
from _reddit.sync_request import TwitchClipSyncRequest
from _reddit.sync_request import TwitchVodSyncRequest


@pytest.mark.parametrize(
    "link, slug",
    [
        (
            "https://clips.twitch.tv/DepressedEnchantingRabbitMrDestructoid",
            "DepressedEnchantingRabbitMrDestructoid",
        ),
        (
            "https://m.twitch.tv/clip/BigSarcasticWalrusRlyTho",
            "BigSarcasticWalrusRlyTho",
        ),
        (
            "https://twitch.tv/CLIP/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
            "ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
        ),
    ],
)
def test_link_TwitchClipSyncRequest_valid(link, slug):
    valid_link = validate_link(link)
    assert valid_link is not None
    assert isinstance(valid_link, TwitchClipSyncRequest)
    assert valid_link.slug == slug


@pytest.mark.parametrize(
    "link, videoId, offsetSeconds",
    [
        (
            "https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=12h50m0s",
            "992654496",
            46200,
        ),
        ("https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=12h50m", "992654496", 46200),
        ("https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=12h50s", "992654496", 43250),
        ("https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=5m50s", "992654496", 350),
        ("https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=9h", "992654496", 32400),
        ("https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=49m", "992654496", 2940),
        ("https://www.twitch.tv/sykkuno/V/992654496?sr=a&t=23s", "992654496", 23),
        ("https://www.twitch.tv/videos/992654496?sr=a&t=23397s", "992654496", 23397),
        ("https://m.twitch.tv/sykkuno/v/992654496?sr=a&t=50m", "992654496", 3000),
        ("https://m.twitch.tv/VIDEOS/992654496?sr=a&t=1h30m", "992654496", 5400),
        ("https://m.twitch.tv/videos/992654496?t=5m500s&", "992654496", 800),
    ],
)
def test_link_TwitchVodSyncRequest_valid(link, videoId, offsetSeconds):
    valid_link = validate_link(link)
    assert valid_link is not None
    assert isinstance(valid_link, TwitchVodSyncRequest)
    assert valid_link.video_id == videoId
    assert valid_link.offset_seconds == offsetSeconds


@pytest.mark.parametrize(
    "link",
    [
        "https://clips.twitch.com/DepressedEnchantingRabbitMrDestructoid",
        "https://clips.twitch.tv/",
        "https://youtube.com/clip/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
        "https://twitch.tv/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V",
        "https://www.twitch.tv/videos/992654496",
        "https://m.twitch.tv/sykkuno/992654496?sr=a&t=23397s",
        "992654496?sr=a&t=23397s",
        "",
    ],
)
def test_link_validator_invalid(link):
    invalid_link = validate_link(link)
    assert isinstance(invalid_link, InvalidSyncRequest)
