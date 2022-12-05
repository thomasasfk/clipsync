from _twitch.queries import broadcaster_id_from_video_id
from _twitch.queries import create_clip_mutation
from _twitch.queries import publish_clip_mutation


def create_twitch_clip(video_id, offset_seconds, broadcaster_id=None, title=""):
    if not broadcaster_id:
        broadcaster_id = broadcaster_id_from_video_id(video_id)
        broadcaster_id = (
            broadcaster_id.get("video", {}).get("owner", {}).get("id", None)
        )
    offset_seconds += 80  # This is needed for the realistic offset
    created_clip = create_clip_mutation(broadcaster_id, video_id, offset_seconds)
    clip_slug = created_clip.get("createClip", {}).get("clip", {}).get("slug", None)
    if clip_slug:
        return publish_clip_mutation(clip_slug, title)
