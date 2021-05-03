from collections import namedtuple

import praw
import yaml
import pymongo
import time

from reddit.src.handleComment import handleComment

POLLING_TIME = 5
# todo: use database for caching and validating vs existing requests
# todo: alternate host.docker.internal/localhost based on docker/local
database = pymongo.MongoClient("host.docker.internal", 27017).clipsync


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

    while True:
        for comment in reddit.subreddit(subredditsUnion).comments(limit=100):
            result = handleComment(comment, botUsername)
            if result:
                print(result)

        time.sleep(POLLING_TIME)
        print("polling again.")
        # todo: handle mentions too?
