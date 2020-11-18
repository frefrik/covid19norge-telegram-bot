from time import sleep
from datetime import datetime, date, timedelta
from telegram import ParseMode
from modules.utils import load_config, get_messagetext, get_timestr
from modules.utils import file_open, file_write
import modules.rss as rss
import modules.graphs as graphs
import modules.c19api as c19api

cfg = load_config()
bot = cfg['bot']
jobs = bot['autopost']['jobs']


def stats(context):
    yesterday = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')

    # metadata
    tested = c19api.metadata('tested')
    confirmed = c19api.metadata('confirmed')
    dead = c19api.metadata('dead')
    admissions = c19api.metadata('admissions')
    respiratory = c19api.metadata('respiratory')

    # totals
    tested_total = tested.get('total')
    confirmed_total = confirmed.get('total')
    dead_total = dead.get('total')
    admissions_total = admissions.get('total')
    respiratory_total = respiratory.get('total')

    # newYesterday
    tested_newYesterday = tested.get('newYesterday', 0)
    confirmed_newYesterday = confirmed.get('newYesterday', 0)
    dead_newYesterday = dead.get('newYesterday', 0)

    # newSince
    confirmed_newSince_d7 = confirmed.get('newSince_d8', 0)
    confirmed_newSince_d14 = confirmed.get('newSince_d15', 0)

    # percentages
    dead_pct = round(dead_total / confirmed_total * 100, 1)
    respiratory_pct = round(respiratory_total / admissions_total * 100, 1)

    ret_str = f"🔢 <b>Nøkkeltall - {yesterday}</b>"
    ret_str += f"\n\n🦠 Smittetilfeller siste døgn: <b>{confirmed_newYesterday:,}</b>"
    ret_str += f"\nSiste 7d: <b>{confirmed_newSince_d7:,}</b>"
    ret_str += f"\nSiste 14d: <b>{confirmed_newSince_d14:,}</b>"
    ret_str += f"\nTotalt: <b>{confirmed_total:,}</b>"
    ret_str += f"\n\n❗ Dødsfall siste døgn: <b>{dead_newYesterday:,}</b>"
    ret_str += f"\nTotalt: <b>{dead_total:,}</b> ({dead_pct}% av smittede)"
    ret_str += f"\n\n🔬 Testede siste døgn: <b>{tested_newYesterday:,}</b>"
    ret_str += f"\nTotalt: <b>{tested_total:,}</b>"
    ret_str += f"\n\n🏥 Innlagt på sykehus: <b>{admissions_total:,}</b>"
    ret_str += f"\n😷 Tilkoblet respirator: <b>{respiratory_total:,}</b> ({respiratory_pct}% av innlagte)"

    ret_str = ret_str.replace(',', ' ')

    context.bot.send_message(
        chat_id=bot['autopost']['chatid'],
        text=ret_str,
        parse_mode=ParseMode.HTML)


def tested(context):
    timestr = get_timestr()
    data = c19api.metadata('tested')
    total = data.get('total')

    last_data = file_open('tested')

    tested_diff = total - int(last_data)

    if tested_diff > 0:
        messagetext = get_messagetext('tested', tested_diff)

        ret_str = f"{timestr} - 🔬 <b>{tested_diff:,}</b> {messagetext}"

        if datetime.now().hour in range(0, 2):
            newYesterday = data.get('newYesterday')

            ret_str += f"\n{timestr} - Totalt: <b>{total:,}</b> (Nye siste døgn: <b>{newYesterday:,}</b>)"
        else:
            newToday = data.get('newToday')

            ret_str += f"\n{timestr} - Totalt: <b>{total:,}</b> (Nye i dag: <b>{newToday:,}</b>)"

        file_write('tested', total)

        ret_str = ret_str.replace(',', ' ')
        print(ret_str, '\n')

        context.bot.send_message(
            chat_id=bot['autopost']['chatid'],
            text=ret_str,
            parse_mode=ParseMode.HTML)
    else:
        return None


def confirmed(context):
    timestr = get_timestr()
    data = c19api.metadata('confirmed')
    total = data.get('total')

    last_data = file_open('confirmed')

    confirmed_diff = total - int(last_data)

    if confirmed_diff > 0:
        messagetext = get_messagetext('confirmed', confirmed_diff)

        ret_str = f"{timestr} - 🦠 <b>{confirmed_diff}</b> {messagetext}"

        if datetime.now().hour in range(0, 2):
            newYesterday = data.get('newYesterday')

            ret_str += f"\n{timestr} - Totalt: <b>{total:,}</b> (Nye siste døgn: <b>{newYesterday:,}</b>)"
        else:
            newToday = data.get('newToday')

            ret_str += f"\n{timestr} - Totalt: <b>{total:,}</b> (Nye i dag: <b>{newToday:,}</b>)"

        file_write('confirmed', total)

        ret_str = ret_str.replace(',', ' ')
        print(ret_str, '\n')

        context.bot.send_message(
            chat_id=bot['autopost']['chatid'],
            text=ret_str,
            parse_mode=ParseMode.HTML)
    else:
        return None


def dead(context):
    timestr = get_timestr()
    data = c19api.metadata('dead')
    total = data.get('total')

    last_data = file_open('dead')

    dead_diff = total - int(last_data)

    if dead_diff > 0:
        messagetext = get_messagetext('dead', dead_diff)

        ret_str = f"{timestr} - ❗ <b>{dead_diff}</b> {messagetext}"

        if datetime.now().hour in range(0, 2):
            newYesterday = data.get('newYesterday')

            ret_str += f"\n{timestr} - Totalt: <b>{total:,}</b> (Nye siste døgn: <b>{newYesterday:,}</b>)"
        else:
            newToday = data.get('newToday')

            ret_str += f"\n{timestr} - Totalt: <b>{total:,}</b> (Nye i dag: <b>{newToday:,}</b>)"

        file_write('dead', total)

        ret_str = ret_str.replace(',', ' ')
        print(ret_str, '\n')

        context.bot.send_message(
            chat_id=bot['autopost']['chatid'],
            text=ret_str,
            parse_mode=ParseMode.HTML)
    else:
        return None


def admissions(context):
    timestr = get_timestr()
    total = c19api.metadata('admissions', 'total')

    last_data = file_open('admissions')

    diff = total - int(last_data)

    if diff != 0:
        if total == 1:
            messagetext = 'person er innlagt på sykehus'
        else:
            messagetext = 'personer er innlagt på sykehus'

        ret_str = f"{timestr} - 🏥 Endring i antall innlagte: <b>{diff:+}</b>"
        ret_str += f"\n{timestr} - <b>{total:,}</b> {messagetext}"

        file_write('admissions', total)

        ret_str = ret_str.replace(',', ' ')
        print(ret_str, '\n')

        context.bot.send_message(
            chat_id=bot['autopost']['chatid'],
            text=ret_str,
            parse_mode=ParseMode.HTML)
    else:
        return None


def respiratory(context):
    timestr = get_timestr()
    total = c19api.metadata('respiratory', 'total')

    last_data = file_open('respiratory')

    diff = total - int(last_data)

    if diff != 0:
        if total == 1:
            messagetext = 'person er på respirator'
        else:
            messagetext = 'personer er på respirator'

        ret_str = f"{timestr} - 😷 Endring i antall på respirator: <b>{diff:+}</b>"
        ret_str += f"\n{timestr} - <b>{total:,}</b> {messagetext}"

        file_write('respiratory', total)

        ret_str = ret_str.replace(',', ' ')
        print(ret_str, '\n')

        context.bot.send_message(
            chat_id=bot['autopost']['chatid'],
            text=ret_str,
            parse_mode=ParseMode.HTML)
    else:
        return None


def rss_fhi(context):
    res = rss.fhi()
    if res is not None:
        context.bot.send_message(
            chat_id=bot['autopost']['chatid'],
            text=res,
            parse_mode=ParseMode.HTML)


def rss_regjeringen(context):
    res = rss.regjeringen()
    if res is not None:
        context.bot.send_message(
            chat_id=bot['autopost']['chatid'],
            text=res,
            parse_mode=ParseMode.HTML)


def graph_all(context):
    chat_id = bot['autopost']['chatid']

    context.bot.send_photo(chat_id, graphs.tested())
    sleep(2)
    context.bot.send_photo(chat_id, graphs.confirmed())
    sleep(2)
    context.bot.send_photo(chat_id, graphs.dead())
    sleep(2)
    context.bot.send_photo(chat_id, graphs.hospitalized())
