import praw
import yaml
import time
import logging

from reddit.src.handleComment import handleComment

logging.basicConfig(filename='debug.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

POLLING_TIME = 5

# # todo: use database for caching and validating vs existing requests
# # todo: alternate host.docker.internal/localhost based on docker/local
# database = pymongo.MongoClient("host.docker.internal", 27017).clipsync

def init_praw():
    praw_config = config.get('praw')
    return praw.Reddit(
        username=praw_config.get('username'),
        password=praw_config.get('password'),
        client_id=praw_config.get('client_id'),
        client_secret=praw_config.get('client_secret'),
        user_agent=praw_config.get('user_agent')
    )


if __name__ == "__main__":
    config = yaml.safe_load(open("config.yml"))
    reddit = init_praw()
    subreddits = config.get('subreddits')
    # todo: test that this works with large number of subreddits
    subredditsUnion = "+".join(subreddits)
    botUsername = config.get('praw').get('username')

    # todo: cache these in a database rather than memory
    seenComments = set()
    seenMentions = set()

    while True:

        try:

            for comment in reddit.subreddit(subredditsUnion).comments(limit=100):
                if comment.id not in seenComments:
                    seenComments.add(comment.id)
                    try:
                        reply = handleComment(comment, botUsername)
                    except Exception as e:
                        logging.error(e)
            if (len(seenComments)) > 2000:
                seenComments.clear()

            for mention in reddit.inbox.mentions(limit=100):
                if mention.id not in seenMentions:
                    seenMentions.add(mention.id)
                    try:
                        reply = handleComment(mention, botUsername)
                    except Exception as e:
                        logging.error(e)
            if (len(seenMentions)) > 2000:
                seenMentions.clear()

            time.sleep(POLLING_TIME)
            print("polling again.")

        except Exception as e:
            logging.error(e)
