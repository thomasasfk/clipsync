from abc import abstractmethod, ABC
import re

from ..src.syncRequest import TwitchClipSyncRequest, TwitchVodSyncRequest
from twitch.src.utils import timestampToSeconds

TWITCH_CLIP_REGEX = re.compile(r'''(?:(?<=twitch.tv/clip/)|(?<=clips.twitch.tv/))[\w\-_]+(?=\?|$|\n)''',
                               re.IGNORECASE)
TWITCH_VOD_REGEX = re.compile(r'''(?:(?<=/videos/)|(?<=/v/))(\d+)(?=\?)|(?<=t=)(\d+s|\d+m|\d+h)(?=&|$)''',
                              re.IGNORECASE)


class Validator(object):
    def __init__(self):
        self.nextHandler = None

    def set_next(self, nextHandler):
        self.nextHandler = nextHandler
        return nextHandler

    def validate(self, link):
        matches = self.matchRegex.findall(link)
        if self.matchCondition(matches):
            return self.syncRequest(matches)
        return self.nextHandler.validate(link)

    @property
    @abstractmethod
    def matchRegex(self):
        """ returns a regex for matching """

    @abstractmethod
    def matchCondition(self, matches):
        """ returns a match condition """""

    @abstractmethod
    def syncRequest(self, matches):
        """ returns a sync request object """


class TwitchClip(Validator):
    matchRegex = TWITCH_CLIP_REGEX

    def syncRequest(self, matches):
        slug = matches[0]
        return TwitchClipSyncRequest(slug)

    def matchCondition(self, matches):
        return len(matches) == 1


class TwitchVod(Validator):
    matchRegex = TWITCH_VOD_REGEX

    def syncRequest(self, matches):
        videoID = [vID for vID in matches[0] if vID][0]
        timestamp = [ts for ts in matches[1] if ts][0]
        offsetSeconds = timestampToSeconds(timestamp)
        return TwitchVodSyncRequest(videoID, offsetSeconds)

    def matchCondition(self, matches):
        return len(matches) == 2


# todo: logging?
class ErrorHandler(Validator, ABC):
    def validate(self, req):
        return False


validatorChain = TwitchClip()

validatorChain.set_next(TwitchVod()) \
    .set_next(ErrorHandler())


def validate(link: str):
    return validatorChain.validate(link)
