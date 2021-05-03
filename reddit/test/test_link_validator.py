import pytest

from reddit.src.link_validator import validate

links = [
    ("https://clips.twitch.tv/DepressedEnchantingRabbitMrDestructoid", True),
    ("https://m.twitch.tv/clip/BigSarcasticWalrusRlyTho", True),
    ("https://twitch.tv/clip/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V", True),
    ("https://www.twitch.tv/sykkuno/v/992654496?sr=a&t=23397s", True),
    ("https://www.twitch.tv/videos/992654496?sr=a&t=23397s", True),
    ("https://m.twitch.tv/sykkuno/v/992654496?sr=a&t=23397s", True),
    ("https://m.twitch.tv/videos/992654496?sr=a&t=23397s", True),
    ("https://m.twitch.tv/videos/992654496?t=23397s&", True),

    ("https://clips.twitch.com/DepressedEnchantingRabbitMrDestructoid", False),
    ("https://clips.twitch.tv/", False),
    ("https://youtube.com/clip/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V", False),
    ("https://twitch.tv/ConsiderateTenuousPuppyBibleThump-oNCm_1UCDInnfn-V", False),
    ("https://www.twitch.tv/videos/992654496", False),
    ("https://m.twitch.tv/sykkuno/992654496?sr=a&t=23397s", False),
    ("992654496?sr=a&t=23397s", False),
    ("", False),
]


@pytest.mark.parametrize("link, is_valid", links)
def test_link_validator(link, is_valid):
    valid_link = validate(link)
    assert valid_link is not None
