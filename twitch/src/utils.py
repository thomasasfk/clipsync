import re

from datetime import datetime, timedelta
from typing import Optional, Match

TWITCH_LOGIN = re.compile(r'''[a-zA-Z0-9-_]{1,25}$''')


def parseTime(time) -> datetime:
    return datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')


def addOffsetToStart(time, videoOffsetSeconds) -> datetime:
    return time + timedelta(seconds=videoOffsetSeconds)


def findIntervalTime(videoOffsetSeconds, createdAt) -> datetime:
    originalVodStart = parseTime(createdAt)
    return addOffsetToStart(originalVodStart, videoOffsetSeconds)


def clipTime(clipInfo):
    videoOffsetSeconds = clipInfo['clip']['videoOffsetSeconds']
    createdAt = clipInfo['clip']['video']['createdAt']
    return findIntervalTime(videoOffsetSeconds, createdAt)


def validLoginFormat(login) -> Optional[Match[str]]:
    return TWITCH_LOGIN.fullmatch(login)


def secondsToTimestamp(time, zeros=False) -> str:
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

    result = '-' if absolute else ''
    result = add_timestamp(hour, result, 'h', zeros)
    result = add_timestamp(minutes, result, 'm', zeros)
    result = add_timestamp(seconds, result, 's', zeros)

    return result or '0s'


def add_timestamp(hms, result, hms_, zeros) -> str:
    if hms > 0:
        result += f'{hms}{hms_}'
    elif zeros:
        result += f'0{hms_}'
    return result


HOURS = re.compile(r'\d+(?=h)')
MINUTES = re.compile(r'\d+(?=m)')
SECONDS = re.compile(r'\d+(?=s)')


def timestampToSeconds(timestamp) -> int:
    totalSeconds = 0
    hours = HOURS.findall(timestamp)
    for hourStamp in hours:
        hourStamp = int(hourStamp)
        totalSeconds += (hourStamp * 3600)
    minutes = MINUTES.findall(timestamp)
    for minuteStamp in minutes:
        minuteStamp = int(minuteStamp)
        totalSeconds += (minuteStamp * 60)
    seconds = SECONDS.findall(timestamp)
    for secondStamp in seconds:
        secondStamp = int(secondStamp)
        totalSeconds += secondStamp
    return totalSeconds
