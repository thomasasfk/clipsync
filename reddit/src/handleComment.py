from twitch.src.sync import Sync
from ..src.linkValidator import validate as isValidLink


def handleComment(comment, botUsername):

    botUsername = 'u/' + botUsername
    if botUsername.lower() not in comment.body.lower():
        return

    syncRequest = isValidLink(comment.link_url)
    if not syncRequest:
        return

    intervalTime = syncRequest.retrieveIntervalTime()
    if not intervalTime:
        return

    newSync = Sync(comment.body.split())
    results = newSync.syncAll(intervalTime)
    if not results:
        return

    return results
    # todo: handle comment responses
    # todo: proper error handling logs
