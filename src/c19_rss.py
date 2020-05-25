import feedparser
import os
from sqlitedict import SqliteDict
from telegram import ParseMode
from c19_utils import load_config

class RSS:
    def __init__(self):
        self.db = SqliteDict('./database.sqlite', 'rss', autocommit=True)
        self.settings = load_config()

    def select_all(self):
        data =  self.db

        for i in data.items():
            print(i)

    def contains_wanted(self, in_str):
        for key_word in self.key_words:
            if key_word.lower() in in_str:
                return True

        return False

    def fhi(self, context):
        feed_url = 'https://fhi.no/rss/nyheter/'
        feed = feedparser.parse(feed_url)

        self.key_words = ['Status koronasmitte', 'koronavirus', 'intensiv', 'covid-19', 'covid19', 'Smittestopp', 'app', 'appen']

        for post in feed.entries:
            title = post.title
            url = post.link
            content = post.description

            if post.link in self.db:
                break

            if self.contains_wanted(title.lower()):
                ret_str = '\n<b>{}</b>'.format(title)
                ret_str += '\n{}'.format(content)
                ret_str += '\n\n{}'.format(url)

                self.db[post.link] = True

            else:
                return None

            context.bot.send_message(chat_id=self.settings['bot']['autopost']['chatid'],
                            text=ret_str,
                            parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    rss = RSS()

    rss.select_all()