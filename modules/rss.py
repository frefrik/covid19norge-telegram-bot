import feedparser
from sqlitedict import SqliteDict

db = SqliteDict('./data/rss_database.sqlite', 'rss', autocommit=True)

regjeringen_key_words = ['pressekonferanse']

key_words = ['korona',
             'intensiv',
             'covid',
             'smitte',
             'app',
             'rød',
             'grøn',
             'hurtigrut',
             'utbrudd',
             'karantene',
             'reiser']


def select_all():
    for i in db.items():
        print(i)


def contains_wanted(in_str):
    for key_word in key_words:
        if key_word.lower() in in_str:
            return True

    return False


def regjeringen_contains_wanted(in_str):
    for key_word in regjeringen_key_words:
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


def regjeringen():
    feed_url = 'https://www.regjeringen.no/no/rss/Rss/2581966/?topic=2692388&documentType=aktuelt/nyheter'
    feed = feedparser.parse(feed_url)

    for post in feed.entries:
        title = post.title
        url = post.link.split("?utm_source")[0]
        content = post.description

        if url in db:
            break

        if regjeringen_contains_wanted(title.lower()):
            ret_str = '\n<b>{}</b>'.format(title)
            ret_str += '\n{}'.format(content)
            ret_str += '\n\n{}'.format(url)

            db[url] = True

        else:
            return None

        return ret_str
