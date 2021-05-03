from abc import abstractmethod, ABC
from collections import namedtuple
from urllib.parse import parse_qs
from urllib.parse import urlparse
import re

from reddit.src.sync_request import TwitchClipSyncRequest, TwitchVodSyncRequest
from twitch.src.utils import timestampToSeconds

TWITCH_VOD_TIMESTAMP_QUERY_PARAM = 't'
TWITCH_SHORT_VOD_PARAM = '/v/'
TWITCH_LONG_VOD_PARAM = '/videos/'
TWITCH_CLIPS_FULL_URL_CLIP_PARAM = '/clip/'
TWITCH_CLIPS_SU8DOMAIN = 'clips'
TWITCH_TV_URL = 'twitch.tv'

TWITCH_CLIP_REGEX = re.compile('(?:(?<=twitch.tv\/clip\/)|(?<=clips.twitch.tv\/))[\w\-\_]+(?=\?|$|\n)')
TWITCH_VOD_REGEX = re.compile('(?:(?<=(?i)\/videos\/)|(?<=(?i)\/v\/))(\d+)(?=\?)|(?<=t\=)(\d+s|\d+m|\d+h)(?=\&|$)')


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
        return False

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
