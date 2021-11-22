from twitch.src.utils import secondsToTimestamp


def formatResult(username, result, hasAnyClips):
    formattedResult = f"[{username}](https://www.twitch.tv/{username})"
    formattedTimestamp = secondsToTimestamp(time=result[1])
    if hasClip(result):
        formattedResult += f" | [Generated Clip](https://clips.twitch.tv/{result[2]})"
    elif hasAnyClips:
        formattedResult += f" | "
    formattedResult += f" | [{formattedTimestamp}](https://www.twitch.tv/videos/{result[0]}?t={formattedTimestamp})"
    return formattedResult


def hasClip(result):
    return len(result) == 3 and result[2] is not None


def formatResultsTable(results):
    hasAnyClips = any(hasClip(result) for name, result in results.items())

    reply = """
    Username | Clip | Vod
    -------- | ---- | ----
    """ if hasAnyClips else """
    Username | Vod
    -------- | ----
    """

    reply += "\n".join(
        formatResult(name, result, hasAnyClips)
        for name, result in results.items()
    )

    return reply
