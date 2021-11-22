from __future__ import annotations

from twitch.src.queries import CreateClipMutation, PublishClipMutation, BroadcasterIDFromVideoID


class TwitchClipService:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    def createTwitchClip(self, videoID, offsetSeconds, broadcasterID=None, title=""):
        if not broadcasterID:
            broadcasterID = BroadcasterIDFromVideoID.post(videoID)
            broadcasterID = broadcasterID.get('video', {}).get('owner', {}).get('id', None)
        offsetSeconds += 80  # This is needed for the realistic offset
        createdClip = CreateClipMutation.post(broadcasterID, videoID, offsetSeconds)
        clipSlug = createdClip.get('createClip', {}).get('clip', {}).get('slug', None)
        if clipSlug:
            return PublishClipMutation.post(clipSlug, title)

    @classmethod
    def instance(cls) -> TwitchClipService:
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
