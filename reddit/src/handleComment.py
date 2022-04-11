import logging

from praw.models import Comment

from twitch.src.sync import Sync
from twitch.src.utils import secondsToTimestamp
from .formatReply import formatResultsTable
from .syncRequest import InvalidSyncRequest
from ..src.linkValidator import validate as getSyncRequest


FEEDBACK_USERNAME = "wee_tommy"
REPO_URL = "https://github.com/thomasasfk/clipsync"

logging.basicConfig(filename='debug.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


def handleComment(comment: Comment, botUsername: str):
    comment.body = comment.body.replace("\\", "")

    if comment.author.name == botUsername:
        return

    botUsernameMention = 'u/' + botUsername
    if botUsernameMention.lower() not in comment.body.lower():
        return

    comment.refresh()
    for c in comment.replies:
        if c.author.name.lower() == botUsername.lower():
            return

    syncRequest = getSyncRequest(comment)
    if not syncRequest or isinstance(syncRequest, InvalidSyncRequest):
        comment.author.message(f"{botUsernameMention} error",
                               formatError("Invalid link in post for purpose of syncing", comment))
        logging.error(f"Invalid link in post for purpose of syncing: {getHyperlink(comment)}")
        return

    intervalTime = syncRequest.retrieveIntervalTime()
    if not intervalTime:
        comment.author.message(f"{botUsernameMention} error",
                               formatError("Insufficient data to preform sync request", comment))
        logging.error(f"Insufficient data to preform sync request: {getHyperlink(comment)}")
        return

    newSync = Sync(comment.body.split())
    results = newSync.syncAll(intervalTime)
    if not results:
        comment.author.message(f"{botUsernameMention} error",
                               formatError("No results found with streamers specified", comment))
        logging.error(f"No results found with streamers specified: {getHyperlink(comment)}")
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
    footer = "\n---\n\n^(*This is an automated response* )" \
             " ^| "
    footer += f"^[Feedback]" \
              f"(http://www.reddit.com/message/compose/?to={FEEDBACK_USERNAME}&subject=Feedback:&message=%5BPost%5D" \
              f"\({hyperlink}\))" \
              " ^| "
    footer += f"^[Source]" \
              f"({REPO_URL})"
    return footer


def getHyperlink(comment):
    return f"https://reddit.com/comments/{comment.submission.id}//{comment.id}/"


def getTwitchMultivodDetails(originalVodDetails, results):
    originalVodTimestamp = secondsToTimestamp(originalVodDetails[1])
    allSyncedVods = "/".join(result[0] for name, result in results.items())
    return f"\n\n[watch via twitchmultivod]" \
           f"(https://twitchmultivod.com/#/" \
           f"{originalVodDetails[0]}?t={originalVodTimestamp}/{allSyncedVods})\n"
