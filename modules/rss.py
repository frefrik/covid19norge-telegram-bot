import feedparser
import os
from sqlitedict import SqliteDict
from utils import load_config

db = SqliteDict('./data/database.sqlite', 'rss', autocommit=True)
settings = load_config()

key_words = ['Status koronasmitte', 'koronavirus', 'intensiv', 'covid-19', 'covid19', 'Smittestopp', 'app', 'appen']

def select_all():
    for i in db.items():
        print(i)

def contains_wanted(in_str):
    for key_word in key_words:
        if key_word.lower() in in_str:
            return True

    return False

def fhi():
    feed_url = 'https://fhi.no/rss/nyheter/'
    feed = feedparser.parse(feed_url)

    for post in feed.entries:
        title = post.title
        url = post.link
        content = post.description

        if post.link in db:
            break

        if contains_wanted(title.lower()):
            ret_str = '\n<b>{}</b>'.format(title)
            ret_str += '\n{}'.format(content)
            ret_str += '\n\n{}'.format(url)

            db[post.link] = True

        else:
            return None

        return ret_str
