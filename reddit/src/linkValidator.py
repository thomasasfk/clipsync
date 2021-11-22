from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Any
import re

from praw.reddit import Comment

from ..src.syncRequest import TwitchClipSyncRequest, TwitchVodSyncRequest, InvalidSyncRequest, SyncRequest
from twitch.src.utils import timestampToSeconds

TWITCH_CLIP_REGEX = re.compile(r'''(?:(?<=twitch.tv/clip/)|(?<=clips.twitch.tv/))[\w\-_]+(?=\?|$|\n)''',
                               re.IGNORECASE)
TWITCH_VOD_REGEX = re.compile(r'''(?:(?<=/videos/)|(?<=/v/))(\d+)(?=\?)|(?<=t=)(\d+s|\d+m|\d+h)(?=&|$)''',
                              re.IGNORECASE)


class Validator(ABC):
    def __init__(self):
        self._nextHandler = None

    def set_next(self, nextHandler: Validator) -> Validator:
        self._nextHandler = nextHandler
        return nextHandler

    @abstractmethod
    def validate(self, link: str) -> SyncRequest:
        """ determines if a link is valid, if valid then it will return a SyncRequest """


class RegexValidator(Validator):

    def validate(self, link: str) -> SyncRequest:
        matches = self._matchRegex.findall(link)
        if self._matchCondition(matches):
            return self._syncRequest(matches)
        return self._nextHandler.validate(link)

    @property
    @abstractmethod
    def _matchRegex(self):
        """ returns a regex for matching """

    @abstractmethod
    def _matchCondition(self, matches: List[Any]) -> bool:
        """ returns a match condition """""

    @abstractmethod
    def _syncRequest(self, matches: List[Any]) -> SyncRequest:
        """ returns a sync request object """


class TwitchClip(RegexValidator):
    _matchRegex = TWITCH_CLIP_REGEX

    def _syncRequest(self, matches) -> TwitchClipSyncRequest:
        slug = matches[0]
        return TwitchClipSyncRequest(slug)

    def _matchCondition(self, matches) -> bool:
        return len(matches) == 1


class TwitchVod(RegexValidator):
    _matchRegex = TWITCH_VOD_REGEX

    def _syncRequest(self, matches):
        videoID = [vID for vID in matches[0] if vID][0]
        timestamp = [ts for ts in matches[1] if ts][0]
        offsetSeconds = timestampToSeconds(timestamp)
        return TwitchVodSyncRequest(videoID, offsetSeconds)

    def _matchCondition(self, matches) -> bool:
        return len(matches) == 2


class ErrorHandler(Validator):
    def validate(self, link: str) -> InvalidSyncRequest:
        return InvalidSyncRequest()


validatorChain = TwitchClip()
validatorChain.set_next(TwitchVod()) \
    .set_next(ErrorHandler())


def validate(comment: Comment) -> SyncRequest:
    try:
        link = comment.link_url
        return validateLink(link)
    except AttributeError:
        pass


def validateLink(link: str) -> SyncRequest:
    return validatorChain.validate(link)
