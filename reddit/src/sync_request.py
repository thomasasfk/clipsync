from abc import abstractmethod, ABC

from twitch.src.queries import ClipInfo, VodCreatedAt
from twitch.src.utils import findIntervalTime


class SyncRequest(ABC):
    @abstractmethod
    def retrieveIntervalTime(self):
        """" fetches required data for syncing """


class TwitchClipSyncRequest(SyncRequest):
    def __init__(self, slug):
        self.slug = slug

    def retrieveIntervalTime(self):
        clipInfo = ClipInfo.post(slug=self.slug)
        try:
            videoOffsetSeconds = clipInfo['clip']['videoOffsetSeconds']
            createdAt = clipInfo['clip']['video']['createdAt']
            return findIntervalTime(videoOffsetSeconds, createdAt)
        except:
            return False


class TwitchVodSyncRequest(SyncRequest):
    def __init__(self, videoId, offsetSeconds):
        self.videoID = videoId
        self.offsetSeconds = offsetSeconds

    def retrieveIntervalTime(self):
        createdAt = VodCreatedAt.post(slug=self.videoID)
        try:
            createdAt = createdAt['video']['createdAt']
            return findIntervalTime(self.offsetSeconds, createdAt)
        except:
            return False
