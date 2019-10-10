import praw
import pickle
import redis
import config
import time
import logging

delay = 30

config_data = config.Config()

reddit = praw.Reddit(client_id=config_data.client_id,
                     client_secret=config_data.client_secret,
                     user_agent='RedditKeywordTracker')

db = redis.Redis(host=config_data.redis_host, port=6379, db=0)


def update_data():
    db_keys = sorted(db.keys())
    old_keys = [key for key in db_keys if key != db_keys[len(db_keys)-1]]
    for key in old_keys:
        db.delete(key)
        print(f"deleted {key}")

    subreddit = reddit.subreddit('all')
    titles = [post.title for post in subreddit.hot(limit=config_data.limit)]
    logging.warning(f"Got {len(titles)} titles")
    db.set(f"titles_{int(time.time())}", pickle.dumps(titles))
    db.set("enabled", 1, ex=config_data.delay)


while True:
    logging.warning("Updating data!")
    update_data()
    logging.warning("Done!")
    time.sleep(config_data.delay)
