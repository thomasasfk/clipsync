import logging
import time

import praw
from praw.reddit import Comment

import config
from _reddit.handle_comment import handle_comment

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s",
)

POLLING_TIME = 5


def init_praw():
    return praw.Reddit(
        username=config.REDDIT.USERNAME,
        password=config.REDDIT.PASSWORD,
        client_id=config.REDDIT.CLIENT_ID,
        client_secret=config.REDDIT.CLIENT_SECRET,
        user_agent=config.REDDIT.USER_AGENT,
    )


if __name__ == "__main__":
    reddit = init_praw()

    subreddits_union = "+".join(config.REDDIT.SUBREDDITS)

    seen_comments = set()

    while True:
        try:
            for mention in reddit.inbox.mentions(limit=100):
                if mention.id not in seen_comments and isinstance(mention, Comment):
                    mention.mark_read()
                    seen_comments.add(mention.id)
                    try:
                        reply = handle_comment(mention)
                    except Exception as e:
                        logging.error(e)

            for comment in reddit.subreddit(subreddits_union).comments(limit=100):
                if comment.id not in seen_comments:
                    seen_comments.add(comment.id)
                    try:
                        reply = handle_comment(comment)
                    except Exception as e:
                        logging.error(e)

            if (len(seen_comments)) > 2000:
                seen_comments.clear()

            print(len(seen_comments))
            time.sleep(POLLING_TIME)
            print("polling again.")

        except Exception as e:
            logging.error(e)
