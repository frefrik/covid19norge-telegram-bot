import yaml
import pandas as pd
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

def get_nordic_df():
    nordic_ts = vg.get_json('nordic_ts')
    ts_se = nordic_ts['countries']['se']
    ts_dk = nordic_ts['countries']['dk']
    ts_no = nordic_ts['countries']['no']

    df_se = pd.DataFrame(ts_se)
    df_dk = pd.DataFrame(ts_dk)
    df_no = pd.DataFrame(ts_no).replace('Norway', 'Norge')

    frames = [df_se, df_dk, df_no]

    df = pd.concat(frames).reset_index(drop=True)
    df = df.rename(columns={'area': 'Land'})
    df['date'] = pd.to_datetime(df['date'])

    return df

def get_timeseries_df():
    region = vg.get_json('region')
    ts_new = region['timeseries']['new']
    ts_total = region['timeseries']['total']
    
    df_new = pd.DataFrame(ts_new)
    df_new = df_new.reset_index()
    df_new.rename(columns={'index': 'date',
                           'confirmed': 'new_confirmed',
                           'dead': 'new_dead',
                           'deadByDateDead': 'new_deadByDateDead'}, 
                           inplace=True)


    df_total = pd.DataFrame(ts_total)
    df_total = df_total.reset_index()
    df_total.rename(columns={'index': 'date',
                             'confirmed': 'total_confirmed',
                             'dead': 'total_dead',
                             'deadByDateDead': 'total_deadByDateDead'}, 
                             inplace=True)

    df = pd.merge(df_new, df_total, how='right', on=['date'])

    return df

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