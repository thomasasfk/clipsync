from _twitch.queries import BroadcasterIDFromVideoID
from _twitch.queries import CreateClipMutation
from _twitch.queries import PublishClipMutation


def create_twitch_clip(video_id, offset_seconds, broadcaster_id=None, title=""):
    if not broadcaster_id:
        broadcaster_id = BroadcasterIDFromVideoID.post(video_id)
        broadcaster_id = (
            broadcaster_id.get("video", {}).get("owner", {}).get("id", None)
        )
    offset_seconds += 80  # This is needed for the realistic offset
    created_clip = CreateClipMutation.post(broadcaster_id, video_id, offset_seconds)
    clip_slug = created_clip.get("createClip", {}).get("clip", {}).get("slug", None)
    if clip_slug:
        return PublishClipMutation.post(clip_slug, title)
