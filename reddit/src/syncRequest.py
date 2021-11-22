from abc import abstractmethod, ABC
from datetime import datetime

from twitch.src.queries import ClipInfo, VodCreatedAt
from twitch.src.utils import findIntervalTime, secondsToTimestamp

import logging
logging.basicConfig(filename='debug.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


class SyncRequest(ABC):
    @abstractmethod
    def retrieveIntervalTime(self) -> datetime:
        """" fetches required data for syncing """

    @abstractmethod
    def retrieveVodDetails(self):
        """" returns timestamped vod """


class InvalidSyncRequest(SyncRequest):
    def retrieveIntervalTime(self) -> None:
        return None

    def retrieveVodDetails(self) -> None:
        return None


class TwitchClipSyncRequest(SyncRequest):
    def __init__(self, slug: str):
        self.slug = slug
        self.videoOffsetSeconds = None

    def retrieveIntervalTime(self) -> datetime:
        clipInfo = ClipInfo.post(slug=self.slug)
        try:
            self.videoOffsetSeconds = clipInfo['clip']['videoOffsetSeconds']
            self.vodId = clipInfo['clip']['video']['id']
            createdAt = clipInfo['clip']['video']['createdAt']
            return findIntervalTime(self.videoOffsetSeconds, createdAt)
        except (TypeError, AttributeError) as e:
            logging.error(f"Error retrieving interval time for: {self.slug}, error: {e}")

    def retrieveVodDetails(self):
        return self.vodId, self.videoOffsetSeconds


class TwitchVodSyncRequest(SyncRequest):
    def __init__(self, videoId, offsetSeconds):
        self.videoID = videoId
        self.offsetSeconds = offsetSeconds

    def retrieveIntervalTime(self) -> datetime:
        createdAt = VodCreatedAt.post(videoID=self.videoID)
        try:
            createdAt = createdAt['video']['createdAt']
            return findIntervalTime(self.offsetSeconds, createdAt)
        except (TypeError, AttributeError) as e:
            logging.error(f"Error retrieving interval time for: {self.videoID}, {self.offsetSeconds}s, error: {e}")

    def retrieveVodDetails(self):
        return self.videoID, self.offsetSeconds