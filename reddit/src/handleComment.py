from praw.models import Comment

from twitch.src.sync import Sync
from twitch.src.utils import secondsToTimestamp
from .formatReply import formatResultsTable
from ..src.linkValidator import validate as isValidLink


def handleComment(comment: Comment, botUsername):
    comment.body = comment.body.replace("\\", "")

    if comment.author.name == botUsername:
        return

    botUsernameMention = 'u/' + botUsername
    if botUsernameMention.lower() not in comment.body.lower():
        return

    comment.refresh()
    for c in comment.replies:
        if c.author.name == botUsername:
            return

    syncRequest = isValidLink(comment)
    if not syncRequest:
        comment.author.message(f"{botUsernameMention} error",
                               formatError("Invalid link in post for purpose of syncing", comment))
        return

    intervalTime = syncRequest.retrieveIntervalTime()
    if not intervalTime:
        comment.author.message(f"{botUsernameMention} error",
                               formatError("Insufficient data to preform sync request", comment))
        return

    newSync = Sync(comment.body.split())
    results = newSync.syncAll(intervalTime, f"https://redd.it/{comment.submission.id}")
    if not results:
        comment.author.message(f"{botUsernameMention} error",
                               formatError("No results found with streamers specified", comment))
        return

    originalVodDetails = syncRequest.retrieveVodDetails()
    reply = formatResultsTable(results)
    reply += getTwitchMultivodDetails(originalVodDetails, results)
    reply += getFooter(comment)
    comment.reply(reply)
    return reply


def formatError(error, comment):
    return f"{error}\n[Post]" \
           f"({getHyperlink(comment)}){getFooter(comment)}"


def getFooter(comment):
    hyperlink = getHyperlink(comment)
    footer = "\n---\n\n^(*This is an automated response* ) ^| "
    footer += f"^[Feedback]" \
              f"(http://www.reddit.com/message/compose/?to=wee_tommy&subject=Feedback:&message=%5BPost%5D" \
              f"\({hyperlink}\))"
    return footer


def getHyperlink(comment):
    return f"https://reddit.com/comments/{comment.submission.id}//{comment.id}/"


def getTwitchMultivodDetails(originalVodDetails, results):
    originalVodTimestamp = secondsToTimestamp(originalVodDetails[1])
    allSyncedVods = "/".join(result[0] for name, result in results.items())
    return f"\n[watch via twitchmultivod]" \
           f"(https://twitchmultivod.com/#/" \
           f"{originalVodDetails[0]}?t={originalVodTimestamp}/{allSyncedVods})"
