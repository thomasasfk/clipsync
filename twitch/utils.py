import re

from datetime import datetime, timedelta

TWITCH_LOGIN = re.compile(r'''[a-zA-Z0-9-_]{1,25}$''')


def parseTime(time):
    return datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')


def addOffsetToStart(time, videoOffsetSeconds):
    return time + timedelta(seconds=videoOffsetSeconds)


def clipTime(clipInfo):
    videoOffsetSeconds = clipInfo['clip']['videoOffsetSeconds']
    createdAt = clipInfo['clip']['video']['createdAt']
    originalVodStart = parseTime(createdAt)
    return addOffsetToStart(originalVodStart, videoOffsetSeconds)


def validLoginFormat(login):
    return TWITCH_LOGIN.fullmatch(login)


def secondsToTimestamp(time, zeros=False):
    absolute = time < 0
    if absolute: time = abs(time)

    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    hour += day * 24
    
    result = '-' if absolute else ''
    result += '%dh' % hour if hour > 0 else ('0h' if zeros else '')
    result += '%dm' % minutes if minutes > 0 else ('0m' if zeros else '')
    result += '%ds' % seconds if seconds > 0 else ('0s' if zeros else '')

    return result if result else '0s' 
