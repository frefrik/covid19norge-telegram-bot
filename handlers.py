from telegram import ParseMode
from modules.utils import load_config
import modules.graphs as graphs
import modules.c19api as c19api

cfg = load_config()
settings = cfg['bot']


def chatid(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Chatid: {}".format(update.message.chat_id),
        parse_mode=ParseMode.HTML)


def help(update, context):
    menuitems = '<b>' + settings['commands']['title'] + '</b>\n'

    for command in list(settings['commands'].items())[1:]:
        menuitems += command[1] + '\n'

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=menuitems,
        parse_mode=ParseMode.HTML)


def stats(update, context):
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

    # newToday
    tested_newToday = tested.get('newToday', 0)
    confirmed_newToday = confirmed.get('newToday', 0)
    dead_newToday = dead.get('newToday', 0)

    # newYesterday
    tested_newYesterday = tested.get('newYesterday', 0)
    confirmed_newYesterday = confirmed.get('newYesterday', 0)
    dead_newYesterday = dead.get('newYesterday', 0)

    # percentages
    confirmed_pct = round(confirmed_total / tested_total * 100, 1)
    dead_pct = round(dead_total / confirmed_total * 100, 1)
    respiratory_pct = round(respiratory_total / admissions_total * 100, 1)

    ret_str = "<b>COVID-19</b>"
    ret_str += f"\nTestede: <b>{tested_total:,}</b>"
    ret_str += f"\nSmittede: <b>{confirmed_total:,}</b> ({confirmed_pct}% av testede) "
    ret_str += f"\nDøde: <b>{dead_total:,}</b> ({dead_pct}% av smittede)"
    ret_str += "\n\n<b>Pasienter på sykehus</b>"
    ret_str += f"\nInnlagt: <b>{admissions_total:,}</b>"
    ret_str += f"\nTilkoblet respirator: <b>{respiratory_total:,}</b> ({respiratory_pct}% av innlagte)"
    ret_str += f"\n\nTestede i dag: <b>{tested_newToday:,}</b>"
    ret_str += f"\nTestede i går: <b>{tested_newYesterday:,}</b>"
    ret_str += f"\nSmittede i dag: <b>{confirmed_newToday:,}</b>"
    ret_str += f"\nSmittede i går: <b>{confirmed_newYesterday:,}</b>"
    ret_str += f"\nDødsfall i dag: <b>{dead_newToday:,}</b>"
    ret_str += f"\nDødsfall i går: <b>{dead_newYesterday:,}</b>"

    ret_str = ret_str.replace(',', ' ')

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=ret_str,
        parse_mode=ParseMode.HTML)


def tested_graph(update, context):
    context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=graphs.tested())


def confirmed_graph(update, context):
    context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=graphs.confirmed())


def dead_graph(update, context):
    context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=graphs.dead())


def hospitalized_graph(update, context):
    context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=graphs.hospitalized())
