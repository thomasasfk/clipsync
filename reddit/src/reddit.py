from collections import namedtuple

import praw
import yaml
import pymongo

from reddit.src.link_validator import validate as valid_link


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
    # todo: make this a namedtuple/dataclass and use it
    comment_dict = {
        'id': comment.id,
        'author': comment.author.name,
        'link_url': comment.link_url,
        'body': comment.body
    }

    # database.comments.insert_one(obj)


def is_valid_comment(comment_dict):
    bot_username = 'u/' + config.get('praw').get('username')
    if bot_username.lower() not in comment_dict.get('body', '').lower():
        return False

    # todo: parse/validate usernames specified in the body

    if not valid_link(comment_dict.get('link_url', '')):
        return False

    # todo: use existing chain as just url validation and write logic to retrieve timestamp via requests


if __name__ == "__main__":
    reddit = init_praw()
    subreddits = config.get('subreddits')
    # todo: test that this works with large number of subreddits
    subreddits_union = "+".join(subreddits)

    while True:
        for comment in reddit.subreddit(subreddits_union).comments(limit=100):
            handle_comment(comment)

        # todo: handle mentions too?