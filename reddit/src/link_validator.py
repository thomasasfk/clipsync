from collections import namedtuple
from urllib.parse import parse_qs
from urllib.parse import urlparse

TWITCH_VOD_TIMESTAMP_QUERY_PARAM = 't'
TWITCH_SHORT_VOD_PARAM = '/v/'
TWITCH_LONG_VOD_PARAM = '/videos/'
TWITCH_CLIPS_FULL_URL_CLIP_PARAM = '/clip/'
TWITCH_CLIPS_SU8DOMAIN = 'clips'
TWITCH_TV_URL = 'twitch.tv'


class Validator(object):
    def __init__(self):
        self.next_handler = None

    def set_next(self, next_handler):
        self.next_handler = next_handler
        return next_handler

    def validate(self, l_w_p):
        return self.next_handler.validate(l_w_p)


class TwitchClip(Validator):
    def validate(self, l_w_p):
        return True if self.__is_valid(l_w_p) else super().validate(l_w_p)

    @staticmethod
    def __is_valid(l_w_p):
        if l_w_p.link.hostname != f'{TWITCH_CLIPS_SU8DOMAIN}.{TWITCH_TV_URL}':
            return False
        if len(l_w_p.link.path) <= 1:
            return False
        return True


class MobileTwitchClip(Validator):
    def validate(self, l_w_p):
        return True if self.__is_valid(l_w_p) else super().validate(l_w_p)

    @staticmethod
    def __is_valid(l_w_p):
        if not l_w_p.link.hostname.endswith(TWITCH_TV_URL):
            return False
        if not l_w_p.link.path.startswith(TWITCH_CLIPS_FULL_URL_CLIP_PARAM):
            return False
        return True


class TwitchVodShort(Validator):
    def validate(self, l_w_p):
        return True if self.__is_valid(l_w_p) else super().validate(l_w_p)

    @staticmethod
    def __is_valid(l_w_p):
        if not l_w_p.link.hostname.endswith(TWITCH_TV_URL):
            return False
        if l_w_p.params.get(TWITCH_VOD_TIMESTAMP_QUERY_PARAM, None) is None:
            return False
        if TWITCH_SHORT_VOD_PARAM not in l_w_p.link.path:
            return False
        return True


class TwitchVodLong(Validator):
    def validate(self, l_w_p):
        return True if self.__is_valid(l_w_p) else super().validate(l_w_p)

    @staticmethod
    def __is_valid(l_w_p):
        if not l_w_p.link.hostname.endswith(TWITCH_TV_URL):
            return False
        if l_w_p.params.get(TWITCH_VOD_TIMESTAMP_QUERY_PARAM, None) is None:
            return False
        if TWITCH_LONG_VOD_PARAM not in l_w_p.link.path:
            return False
        return True


# todo: logging?
class ErrorHandler(Validator):
    def validate(self, req):
        return False


LinkWithParams = namedtuple('LinkWithParams', ['link', 'params'])

validator_chain = Validator()

validator_chain.set_next(TwitchClip()) \
    .set_next(MobileTwitchClip()) \
    .set_next(TwitchVodShort()) \
    .set_next(TwitchVodLong()) \
    .set_next(ErrorHandler())


def validate(link: str):
    parsed_link = urlparse(link)
    if parsed_link.hostname is None:
        return False

    parsed_params = parse_qs(parsed_link.query)

    u_w_p = LinkWithParams(parsed_link, parsed_params)
    return validator_chain.validate(u_w_p)
