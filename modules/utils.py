import yaml
from datetime import datetime, date, timedelta
from vg import VG

vg = VG()

with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def get_messagetext(name, diff):
    if diff is None:
        return None
    if diff == 1:
        messagetext = cfg['bot']['autopost']['jobs'][name]['text_pos_singular']
    elif diff > 1:
        messagetext = cfg['bot']['autopost']['jobs'][name]['text_pos_plural']
    elif diff == -1:
        messagetext = cfg['bot']['autopost']['jobs'][name]['text_neg_singular']
    elif diff < -1:
        messagetext = cfg['bot']['autopost']['jobs'][name]['text_neg_plural']
    else:
        return None

    return messagetext

def get_timestr():
    timestr = datetime.now().strftime('%H:%M')

    return timestr

def get_yesterday():
    yesterday = int((date.today() - timedelta(days=1)).strftime('%s')) + 7200

    return yesterday

def wait_seconds(interval):
    now = datetime.now()
    next = now + (datetime.min - now) % timedelta(minutes=int(interval))
    sec_wait = (next - now).seconds + 10

    return sec_wait

def midnight_seconds():
    now = datetime.now()
    midnight_delta = timedelta(days=1)
    midnight_next = (now + midnight_delta).replace(hour=0, minute=5, microsecond=0, second=0)
    next_midnight = (midnight_next - now).seconds

    return next_midnight

def load_config():
    with open('./config.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    return cfg