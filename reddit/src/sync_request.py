from abc import abstractmethod, ABC

from twitch.src.queries import ClipInfo, VodCreatedAt
from twitch.src.utils import findIntervalTime

import logging
logging.basicConfig(filename='debug.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


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
        except Exception as e:
            logging.error(f"Error retrieving interval time for: {self.slug}, error: {e}")


class TwitchVodSyncRequest(SyncRequest):
    def __init__(self, videoId, offsetSeconds):
        self.videoID = videoId
        self.offsetSeconds = offsetSeconds

    def retrieveIntervalTime(self):
        createdAt = VodCreatedAt.post(videoID=self.videoID)
        try:
            createdAt = createdAt['video']['createdAt']
            return findIntervalTime(self.offsetSeconds, createdAt)
        except Exception as e:
            logging.error(f"Error retrieving interval time for: {self.videoID}, {self.offsetSeconds}s, error: {e}")
