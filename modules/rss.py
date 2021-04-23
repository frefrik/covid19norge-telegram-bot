import re
import feedparser
from modules.utils import file_open_json, file_write_json


def contains_wanted(in_str, key_words):
    for key_word in key_words:
        if key_word.lower() in in_str:
            return True
    return False


def fetch_feed():
    rssfile = file_open_json("rss")

    for i in rssfile:
        feed_url = rssfile[i]["feed_url"]
        keywords = rssfile[i]["keywords"]
        seen_urls = rssfile[i]["seen_urls"]

        feed = feedparser.parse(feed_url)

        for post in feed.entries:
            title = post.title
            url = post.link
            try:
                content = post.description
                content = re.sub("<[^>]*>", "", content)
            except Exception:
                content = None

            if url not in seen_urls:
                if contains_wanted(title.lower(), keywords):
                    ret_str = f"\n<b>{title}</b>"
                    if content:
                        ret_str += f"\n{content}"
                    ret_str += f"\n\n{url}"
                    print(ret_str)

                    seen_urls.append(url)
                    file_write_json("rss", rssfile)

                    return ret_str
