from _twitch.utils import seconds_to_timestamp


def formatResult(username, result, hasAnyClips):
    formattedResult = f"[{username}](https://www.twitch.tv/{username}/?)"  # question mark is to prevent embed button
    formattedTimestamp = seconds_to_timestamp(time=result[1], zeros=True)
    if hasClip(result):
        formattedResult += f" | [Generated Clip](https://clips.twitch.tv/{result[2]})"
    elif hasAnyClips:
        formattedResult += " | "
    formattedResult += f" | [{formattedTimestamp}](https://www.twitch.tv/videos/{result[0]}?t={formattedTimestamp})"
    return formattedResult


def hasClip(result):
    return len(result) == 3 and result[2] is not None


def format_results_table(results):
    hasAnyClips = any(hasClip(result) for name, result in results.items())

    reply = (
        """Username | Clip | Vod
-------- | ---- | ----
"""
        if hasAnyClips
        else """
Username | Vod
-------- | ----
"""
    )

    reply += "\n".join(
        formatResult(name, result, hasAnyClips) for name, result in results.items()
    )

    return reply
