import logging
import time
import threading
import queue
import praw
import pymongo
import yaml
from praw.reddit import Comment

from reddit.src.handleComment import handleComment

logging.basicConfig(filename='debug.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

POLLING_TIME = 10

# # todo: use database for caching and validating vs existing requests
# # todo: alternate host.docker.internal/localhost based on docker/local
config = yaml.safe_load(open("config.yml"))
mongodb_src = config.get('mongodb').get('srv')
database = pymongo.MongoClient(mongodb_src).clipsync


def init_praw():
    praw_config = config.get('praw')
    return praw.Reddit(
        username=praw_config.get('username'),
        password=praw_config.get('password'),
        client_id=praw_config.get('client_id'),
        client_secret=praw_config.get('client_secret'),
        user_agent=praw_config.get('user_agent')
    )


def commentHandleWorker(q, botUsername):
    while True:
        aComment = q.get()
        try:
            # todo: handle comments, this should just work but its untested
            print(aComment.id, botUsername)
            # handleComment(aComment, botUsername)
        except Exception as e:
            logging.error(e)
        finally:
            q.task_done()
        time.sleep(0.5)


if __name__ == "__main__":
    reddit = init_praw()
    subreddits = config.get('subreddits')
    # todo: test that this works with large number of subreddits
    subredditsUnion = "+".join(subreddits)
    botUsername = config.get('praw').get('username')

    q = queue.Queue()
    threading.Thread(target=commentHandleWorker, args=[q, botUsername], daemon=True).start()

    while True:
        commentsToHandle = []
        currentlyPolledComments = set()

        for mention in reddit.inbox.mentions(limit=20):
            if mention.id not in currentlyPolledComments and isinstance(mention, Comment):
                currentlyPolledComments.add(mention.id)
                commentsToHandle.append(mention)

        for comment in reddit.subreddit(subredditsUnion).comments(limit=50):
            if comment.id not in currentlyPolledComments:
                currentlyPolledComments.add(comment.id)
                commentsToHandle.append(comment)

        previouslyHandledComments = {x['comment_id'] for x in list(database.comments.find({
            'comment_id': {'$in': list(currentlyPolledComments)}
        }))}

        currentCommentsToBeHandled = currentlyPolledComments - previouslyHandledComments
        commentsToHandle = {comment.id:comment for comment in commentsToHandle if comment.id in currentCommentsToBeHandled}

        if currentCommentsToBeHandled:
            database.comments.insert_many([{'comment_id': x} for x in currentCommentsToBeHandled])
            print(f"inserted {len(currentCommentsToBeHandled)} comments being handled.")

        for comment_id, comment in commentsToHandle.items():
            q.put(comment)

        time.sleep(POLLING_TIME)
        print("polling again.")
