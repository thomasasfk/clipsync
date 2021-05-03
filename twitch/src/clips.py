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
            publishedClip = PublishClipMutation.post(clipSlug, title)
            return publishedClip

    # singleton for handling race condition of ratelimits
    # but the code is so slow it doesn't even matter lmao
    # maybe i'll refactor to use proper sessions in future
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
