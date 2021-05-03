from collections import namedtuple

import praw
import yaml
import pymongo
import time

from link_validator import validate as hasValidLink

POLLING_TIME = 5
config = yaml.safe_load(open("config.yml"))
# todo: use database for caching and validating vs existing requests
# todo: alternate host.docker.internal/localhost based on docker/local
database = pymongo.MongoClient("host.docker.internal", 27017).clipsync
UrlWithParams = namedtuple('LinkWithParams', ['link', 'params'])


def init_praw():
    praw_config = config.get('praw')
    return praw.Reddit(
        username=praw_config.get('username'),
        password=praw_config.get('password'),
        client_id=praw_config.get('client_id'),
        client_secret=praw_config.get('client_secret'),
        user_agent=praw_config.get('user_agent')
    )


def handle_comment(comment):
    print(comment)
    # todo: make this a namedtuple/dataclass and use it
    comment_dict = {
        'id': comment.id,
        'author': comment.author.name,
        'link_url': comment.link_url,
        'body': comment.body
    }

    # database.comments.insert_one(obj)


def isValidComment(comment_dict):
    botUsername = 'u/' + config.get('praw').get('username')
    if botUsername.lower() not in comment_dict.get('body', '').lower():
        return False

    syncRequest = hasValidLink(comment_dict.get('link_url', ''))
    if not syncRequest:
        return False

    intervalTime = syncRequest.retrieveIntervalTime()
    if not intervalTime:
        return False


    # todo: parse/validate usernames specified in the body


    # todo: use existing chain as just url validation and write logic to retrieve timestamp via requests


if __name__ == "__main__":
    reddit = init_praw()
    subreddits = config.get('subreddits')
    # todo: test that this works with large number of subreddits
    subredditsUnion = "+".join(subreddits)

    while True:
        for comment in reddit.subreddit(subredditsUnion).comments(limit=100):
            handle_comment(comment)

        # todo: handle mentions too?
        time.sleep(POLLING_TIME)