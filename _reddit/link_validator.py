from __future__ import annotations

import logging
import re
from abc import ABC
from abc import abstractmethod

from praw.reddit import Comment

from _reddit.sync_request import InvalidSyncRequest
from _reddit.sync_request import SyncRequest
from _reddit.sync_request import TwitchClipSyncRequest
from _reddit.sync_request import TwitchVodSyncRequest
from _twitch.utils import timestamp_to_seconds

TWITCH_CLIP_REGEX = re.compile(
    r"""(?:(?<=twitch\.tv/clip/)|(?<=clips\.twitch\.tv/))([\w\-]+)(?=\?|$|\n)""",
    re.IGNORECASE,
)
TWITCH_VOD_REGEX = re.compile(
    r"""twitch\.tv/.*(?:(?<=/v/)|(?<=/videos/))(\d+)(?=\?|$|\n).*?((?:\d+[hms])+)""",
    re.IGNORECASE,
)


class Validator(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, next_handler: Validator) -> Validator:
        self._next_handler = next_handler
        return next_handler

    @abstractmethod
    def validate(self, link: str) -> SyncRequest:
        """determines if a link is valid, if valid then it will return a SyncRequest"""


class RegexValidator(Validator):
    def validate(self, link: str) -> SyncRequest:
        match = self._match_regex.search(link)
        if match:
            return self._sync_request(match)
        return self._next_handler.validate(link)

    @property
    @abstractmethod
    def _match_regex(self):
        """returns a regex for matching"""

    @abstractmethod
    def _sync_request(self, match: re.Match) -> SyncRequest:
        """returns a sync request object"""


class TwitchClip(RegexValidator):
    _match_regex = TWITCH_CLIP_REGEX

    def _sync_request(self, match: re.Match) -> TwitchClipSyncRequest:
        slug = match.group(1)
        return TwitchClipSyncRequest(slug)


class TwitchVod(RegexValidator):
    _match_regex = TWITCH_VOD_REGEX

    def _sync_request(self, match: re.Match):
        video_id, unformatted_timestamp = match.groups()
        offset_seconds = timestamp_to_seconds(unformatted_timestamp)
        return TwitchVodSyncRequest(video_id, offset_seconds)


class ErrorHandler(Validator):
    def validate(self, link: str) -> InvalidSyncRequest:
        logging.info(f"Got to end of chain without matching link: {link}")
        return InvalidSyncRequest()


validator_chain = TwitchClip()
validator_chain.set_next(
    TwitchVod(),
).set_next(
    ErrorHandler(),
)


def get_sync_request(comment: Comment) -> SyncRequest:
    if hasattr(comment, 'link_url'):
        return validate_link(comment.link_url)
    elif hasattr(comment, 'submission') and hasattr(comment.submission, 'url'):
        return validate_link(comment.submission.url)

    logging.info("Unable to extract submission or link url from comment")
    return InvalidSyncRequest()


def validate_link(link: str) -> SyncRequest:
    return validator_chain.validate(link)
