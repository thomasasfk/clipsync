import logging
from abc import ABC
from abc import abstractmethod
from datetime import datetime

from _twitch.queries import ClipInfo
from _twitch.queries import VodCreatedAt
from _twitch.utils import find_interval_time

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s",
)


class SyncRequest(ABC):
    @abstractmethod
    def retrieve_interval_time(self) -> datetime | None:
        """ " fetches required data for syncing"""

    @abstractmethod
    def retrieve_vod_details(self):
        """ " returns timestamped vod"""


class InvalidSyncRequest(SyncRequest):
    def retrieve_interval_time(self) -> None:
        return None

    def retrieve_vod_details(self) -> None:
        return None


class TwitchClipSyncRequest(SyncRequest):
    def __init__(self, slug: str):
        self.slug = slug
        self.video_offset_seconds = None

    def retrieve_interval_time(self) -> datetime | None:
        clip_info = ClipInfo.post(slug=self.slug)
        try:
            self.video_offset_seconds = clip_info["clip"]["videoOffsetSeconds"]
            self.vod_id = clip_info["clip"]["video"]["id"]
            created_at = clip_info["clip"]["video"]["createdAt"]
            return find_interval_time(self.video_offset_seconds, created_at)
        except (TypeError, AttributeError) as e:
            logging.error(
                f"Error retrieving interval time for: {self.slug}, error: {e}",
            )
        return None

    def retrieve_vod_details(self):
        return self.vod_id, self.video_offset_seconds


class TwitchVodSyncRequest(SyncRequest):
    def __init__(self, video_id, offset_seconds):
        self.video_id = video_id
        self.offset_seconds = offset_seconds

    def retrieve_interval_time(self) -> datetime | None:
        created_at = VodCreatedAt.post(video_id=self.video_id)
        try:
            created_at = created_at["video"]["createdAt"]
            return find_interval_time(self.offset_seconds, created_at)
        except (TypeError, AttributeError) as e:
            logging.error(
                f"Error retrieving interval time for: {self.video_id}, {self.offset_seconds}s, error: {e}",
            )
            return None

    def retrieve_vod_details(self):
        return self.video_id, self.offset_seconds
