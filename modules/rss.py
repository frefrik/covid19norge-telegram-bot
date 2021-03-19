import feedparser
from sqlitedict import SqliteDict

db = SqliteDict("./data/rss_database.sqlite", "rss", autocommit=True)

regjeringen_key_words = ["pressekonferanse"]

key_words = [
    "korona",
    "intensiv",
    "covid",
    "smitte",
    "app",
    "rød",
    "grøn",
    "hurtigrut",
    "utbrudd",
    "karantene",
    "reiser",
    "AstraZeneca",
    "Moderna",
    "Comirnaty",
    "BioNTech",
    "Pfizer",
]


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
    feed_url = "https://fhi.no/rss/nyheter/"
    feed = feedparser.parse(feed_url)

    for post in feed.entries:
        title = post.title
        url = post.link
        try:
            content = post.description
        except Exception:
            content = None

        if post.link in db:
            break

        if contains_wanted(title.lower()):
            ret_str = f"\n<b>{title}</b>"
            if content:
                ret_str += f"\n{content}"
            ret_str += f"\n\n{url}"

            db[post.link] = True

        else:
            return None

        return ret_str


def regjeringen():
    feed_url = "https://www.regjeringen.no/no/rss/Rss/2581966/?topic=2692388&documentType=aktuelt/nyheter"
    feed = feedparser.parse(feed_url)

    for post in feed.entries:
        title = post.title
        url = post.link.split("?utm_source")[0]
        try:
            content = post.description
        except Exception:
            content = None

        if url in db:
            break

        if regjeringen_contains_wanted(title.lower()):
            ret_str = f"\n<b>{title}</b>"
            if content:
                ret_str += f"\n{content}"
            ret_str += f"\n\n{url}"

            db[url] = True

        else:
            return None

        return ret_str
