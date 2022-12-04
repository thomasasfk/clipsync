import logging

from praw.models import Comment

import config
from _reddit.format_reply import format_results_table
from _reddit.link_validator import get_sync_request
from _reddit.sync_request import InvalidSyncRequest
from _twitch.sync import Sync
from _twitch.utils import seconds_to_timestamp

FEEDBACK_USERNAME = "wee_tommy"
REPO_URL = "https://github.com/thomasasfk/clipsync"

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s",
)


def handle_comment(comment: Comment) -> tuple[int, str]:
    comment.body = comment.body.replace("\\", "")

    if comment.author.name == config.REDDIT.USERNAME:
        return 0, "Comment is from bot"

    bot_username_mention = "u/" + config.REDDIT.USERNAME
    if bot_username_mention.lower() not in comment.body.lower():
        return 0, "Comment does not mention bot"

    comment.refresh()
    for c in comment.replies:
        if c.author.name.lower() == config.REDDIT.USERNAME.lower():
            return 0, "Comment already replied"

    sync_request = get_sync_request(comment)
    if not sync_request or isinstance(sync_request, InvalidSyncRequest):
        comment.author.message(
            f"{bot_username_mention} error",
            format_error("Invalid link in post for purpose of syncing", comment),
        )
        logging.error(
            f"Invalid link in post for purpose of syncing: {get_hyperlink(comment)}",
        )
        return 0, "Invalid link in post for purpose of syncing"

    interval_time = sync_request.retrieve_interval_time()
    if not interval_time:
        comment.author.message(
            f"{bot_username_mention} error",
            format_error("Insufficient data to preform sync request", comment),
        )
        logging.error(
            f"Insufficient data to preform sync request: {get_hyperlink(comment)}",
        )
        return 0, "Insufficient data to preform sync request"

    new_sync = Sync(comment.body.split())
    results = new_sync.sync_all(interval_time, f"https://redd.it/{comment.submission.id}")
    if not results:
        comment.author.message(
            f"{bot_username_mention} error",
            format_error("No results found with streamers specified", comment),
        )
        logging.error(
            f"No results found with streamers specified: {get_hyperlink(comment)}",
        )
        return 0, "No results found with streamers specified"

    original_vod_details = sync_request.retrieve_vod_details()
    reply = format_results_table(results)
    reply += get_twitch_multivod_details(original_vod_details, results)
    reply += get_footer(comment)

    posted_comment = comment.reply(reply)
    return 0 if posted_comment else 1, reply


def format_error(error, comment):
    return f"{error}\n[Post]({get_hyperlink(comment)}){get_footer(comment)}"


def get_footer(comment):
    hyperlink = get_hyperlink(comment)
    footer = "\n---\n\n^(*This is an automated response* ) ^| "
    footer += (
        f"^[Feedback]"
        f"(http://www.reddit.com/message/compose/?to={FEEDBACK_USERNAME}&subject=Feedback:&message=%5BPost%5D"
        f"\\({hyperlink}\\))"
        " ^| "
    )
    footer += f"^[Source]({REPO_URL})"
    return footer


def get_hyperlink(comment):
    return f"https://reddit.com/comments/{comment.submission.id}//{comment.id}/"


def get_twitch_multivod_details(original_vod_details, results):
    original_vod_timestamp = seconds_to_timestamp(original_vod_details[1])
    all_synced_vods = "/".join(result[0] for name, result in results.items())
    return (
        f"\n\n[watch via twitchmultivod]"
        f"(https://twitchmultivod.com/#/"
        f"{original_vod_details[0]}?t={original_vod_timestamp}/{all_synced_vods})\n"
    )
