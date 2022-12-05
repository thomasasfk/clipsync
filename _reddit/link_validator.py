import logging
import re

from praw.reddit import Comment

from _reddit.sync_request import InvalidSyncRequest
from _reddit.sync_request import SyncRequest
from _reddit.sync_request import TwitchClipSyncRequest
from _reddit.sync_request import TwitchVodSyncRequest
from _twitch.utils import timestamp_to_seconds

TWITCH_CLIP_REGEX = re.compile(
    r"""(?:
        # Match either of the following:
        # - The string 'twitch.tv/clip/'
        # - The string 'clips.twitch.tv/'
        (?<=twitch\.tv/clip/)|(?<=clips\.twitch\.tv/)
    )
    # Capture the following group:
    (
        # Match one or more word characters or dashes
        [\w\-]+
    )
    # Match either of the following:
    # - The end of the string
    # - The character '?'
    # - A newline character
    (?=\?|$|\n)""",
    re.IGNORECASE | re.VERBOSE,
)

TWITCH_VOD_REGEX = re.compile(
    r"""
        twitch\.tv/.*
        # Match either of the following:
        # - The string '/v/'
        # - The string '/videos/'
        (?:(?<=/v/)|(?<=/videos/))
        # Capture the following group:
        (
            # Match one or more digits
            \d+
        )
        # Match either of the following:
        # - The end of the string
        # - The character '?'
        # - A newline character
        (?=\?|$|\n)
        # Match the following group non-greedily:
        .*?
        (
            (?:
                # Match one or more digits followed by one of the characters 'h', 'm', or 's'
                \d+[hms]
            )+
        )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def validate_link(link: str) -> SyncRequest:
    """Validates a link and returns a SyncRequest object."""
    _match = TWITCH_CLIP_REGEX.search(link)
    if _match:
        slug = _match.group(1)
        return TwitchClipSyncRequest(slug)

    _match = TWITCH_VOD_REGEX.search(link)
    if _match:
        video_id, unformatted_timestamp = _match.groups()
        offset_seconds = timestamp_to_seconds(unformatted_timestamp)
        return TwitchVodSyncRequest(video_id, offset_seconds)

    return InvalidSyncRequest()


def get_sync_request(comment: Comment) -> SyncRequest:
    if hasattr(comment, 'link_url'):
        return validate_link(comment.link_url)
    elif hasattr(comment, 'submission') and hasattr(comment.submission, 'url'):
        return validate_link(comment.submission.url)

    logging.info("Unable to extract submission or link url from comment")
    return InvalidSyncRequest()
