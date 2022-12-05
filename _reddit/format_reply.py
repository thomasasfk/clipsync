from _twitch.utils import seconds_to_timestamp


def format_reply(username, result, has_any_clips):
    formatted_result = f"[{username}](https://www.twitch.tv/{username}/?)"  # question mark is to prevent embed button
    formatted_timestamp = seconds_to_timestamp(time=result[1], zeros=True)
    if has_clip(result):
        formatted_result += f" | [Generated Clip](https://clips.twitch.tv/{result[2]})"
    elif has_any_clips:
        formatted_result += " | "
    formatted_result += f" | [{formatted_timestamp}](https://www.twitch.tv/videos/{result[0]}?t={formatted_timestamp})"
    return formatted_result


def has_clip(result):
    return len(result) == 3 and result[2] is not None


def format_results_table(results):
    has_any_clips = any(has_clip(result) for name, result in results.items())

    reply = (
        """Username | Clip | Vod
-------- | ---- | ----
"""
        if has_any_clips
        else """
Username | Vod
-------- | ----
"""
    )

    reply += "\n".join(
        format_reply(name, result, has_any_clips) for name, result in results.items()
    )

    return reply
