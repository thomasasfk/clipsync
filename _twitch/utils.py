import re
from datetime import datetime
from datetime import timedelta
from typing import Match
from typing import Optional

TWITCH_LOGIN = re.compile(r"""[a-zA-Z0-9-_]{1,25}$""")


def parse_time(time) -> datetime:
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")


def add_offset_to_start(time, videoOffsetSeconds) -> datetime:
    return time + timedelta(seconds=videoOffsetSeconds)


def find_interval_time(videoOffsetSeconds, createdAt) -> datetime:
    originalVodStart = parse_time(createdAt)
    return add_offset_to_start(originalVodStart, videoOffsetSeconds)


def clip_time(clip_info):
    video_offset_seconds = clip_info["clip"]["videoOffsetSeconds"]
    createdAt = clip_info["clip"]["video"]["createdAt"]
    return find_interval_time(video_offset_seconds, createdAt)


def valid_login_format(login) -> Optional[Match[str]]:
    return TWITCH_LOGIN.fullmatch(login)


def seconds_to_timestamp(time, zeros=False) -> str:
    time = int(time)
    absolute = time < 0
    if absolute:
        time = abs(time)

    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    hour += day * 24

    result = "-" if absolute else ""
    result = add_timestamp(hour, result, "h", zeros)
    result = add_timestamp(minutes, result, "m", zeros)
    result = add_timestamp(seconds, result, "s", zeros)

    return result or "0s"


def add_timestamp(hms, result, hms_, zeros) -> str:
    if hms > 0:
        result += f"{hms}{hms_}"
    elif zeros:
        result += f"0{hms_}"
    return result


HOURS = re.compile(r"\d+(?=h)")
MINUTES = re.compile(r"\d+(?=m)")
SECONDS = re.compile(r"\d+(?=s)")


def timestamp_to_seconds(timestamp) -> int:
    total_seconds = 0
    hours = HOURS.findall(timestamp)
    for hour_stamp in hours:
        hour_stamp = int(hour_stamp)
        total_seconds += hour_stamp * 3600
    minutes = MINUTES.findall(timestamp)
    for minute_stamp in minutes:
        minute_stamp = int(minute_stamp)
        total_seconds += minute_stamp * 60
    seconds = SECONDS.findall(timestamp)
    for second_stamp in seconds:
        second_stamp = int(second_stamp)
        total_seconds += second_stamp
    return total_seconds
