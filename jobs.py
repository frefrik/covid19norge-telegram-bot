import sys
import yaml
from telegram import ParseMode

sys.path.append('./modules/')
import graphs
import rss
from vg import VG
from utils import get_messagetext, get_timestr, get_yesterday

with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

vg = VG()
settings = cfg['bot']

def stats(context):
    ''' Totals '''
    population = vg.get_data('population', 'total')
    tested = vg.get_data('tested', 'total')
    confirmed = vg.get_data('confirmed', 'total')
    dead = vg.get_data('dead', 'total')
    hospitalized = vg.get_data('hospitalized', 'total')
    intensiveCare = vg.get_data('intensiveCare', 'total')
    respiratory = vg.get_data('respiratory', 'total')
    infectedEmployees = vg.get_data('infectedEmployees', 'total')
    quarantineEmployees = vg.get_data('quarantineEmployees', 'total')

    ''' newToday '''
    tested_newToday = vg.get_data('tested', 'newToday')
    confirmed_newToday = vg.get_data('confirmed', 'newToday')
    dead_newToday = vg.get_data('dead', 'newToday')

    ''' newYesterday '''
    tested_newYesterday = vg.get_data('tested', 'newYesterday')
    confirmed_newYesterday = vg.get_data('confirmed', 'newYesterday')
    dead_newYesterday = vg.get_data('dead', 'newYesterday')

    ''' Percentages '''
    population_pct = round(confirmed / population * 100, 2)
    tested_pct = round(tested / population * 100, 1)
    confirmed_pct = round(confirmed / tested * 100, 1)
    dead_pct = round(dead / confirmed * 100, 1)
    intensiveCare_pct = round(intensiveCare / hospitalized * 100,1)
    respiratory_pct = round(respiratory / hospitalized * 100,1)
    tested_newToday_pct = vg.get_data('tested', 'newToday_pctChg')
    tested_newYesterday_pct = vg.get_data('tested', 'newYesterday_pctChg')
    confirmed_newToday_pct = vg.get_data('confirmed', 'newToday_pctChg')
    confirmed_newYesterday_pct = vg.get_data('confirmed', 'newYesterday_pctChg')
    dead_newToday_pct = vg.get_data('dead', 'newToday_pctChg')
    dead_newYesterday_pct = vg.get_data('dead', 'newYesterday_pctChg')

    ret_str = "<b>COVID-19</b>"
    ret_str += "\nTestede: <b>{}</b>".format(tested)
    ret_str += "\nSmittede: <b>{}</b> ({}% av testede) ".format(confirmed, confirmed_pct)
    ret_str += "\nDøde: <b>{}</b> ({}% av smittede)".format(dead, dead_pct)
    ret_str += "\n\n<b>Pasienter på sykehus</b>"
    ret_str += "\nInnlagt: <b>{}</b>".format(hospitalized)
    ret_str += "\nIntensivbehandling: <b>{}</b> ({}% av innlagte)".format(intensiveCare, intensiveCare_pct)
    ret_str += "\nTilkoblet respirator: <b>{}</b> ({}% av innlagte)".format(respiratory, respiratory_pct)
    ret_str += "\n\nTestede i dag: <b>{}</b> ({:+.02f}%)".format(tested_newToday, tested_newToday_pct)
    ret_str += "\nTestede i går: <b>{}</b> ({:+.02f}%)".format(tested_newYesterday, tested_newYesterday_pct)
    ret_str += "\nSmittede i dag: <b>{}</b> ({:+.02f}%)".format(confirmed_newToday, confirmed_newToday_pct)
    ret_str += "\nSmittede i går: <b>{}</b> ({:+.02f}%)".format(confirmed_newYesterday, confirmed_newYesterday_pct)
    ret_str += "\nDødsfall i dag: <b>{}</b> ({:+.02f}%)".format(dead_newToday, dead_newToday_pct)
    ret_str += "\nDødsfall i går: <b>{}</b> ({:+.02f}%)".format(dead_newYesterday, dead_newYesterday_pct)
    ret_str += "\n\nHelsepersonell smittet: <b>{}</b>".format(infectedEmployees)
    ret_str += "\nHelsepersonell i karantene: <b>{}</b>".format(quarantineEmployees)
    ret_str += "\n\n<b>Kjønnsfordeling smittede</b>"
    ret_str += "\nMenn: {}%".format(vg.get_data('confirmed', 'male'))
    ret_str += "\nKvinner: {}%".format(vg.get_data('confirmed', 'female'))
    ret_str += "\n\n<b>Gjennomsnittsalder</b>"
    ret_str += "\nDe {} første innlagte: <b>{} år</b>".format(vg.get_data('hospitalized', 'totalcases'), vg.get_data('hospitalized', 'age_mean'))
    ret_str += "\nDe {} første innlagte på intensiv: <b>{} år</b>".format(vg.get_data('intensiveCare', 'totalcases'), vg.get_data('intensiveCare', 'age_mean'))
    ret_str += "\nDe {} første dødsfall: <b>{} år</b>".format(vg.get_data('dead', 'totalcases'), vg.get_data('dead', 'age_mean'))
    ret_str += "\n\nAndel av befolkningen testet: <b>{}%</b>".format(tested_pct)
    ret_str += "\nAndel av befolkningen smittet: <b>{}%</b>".format(population_pct)

    context.bot.send_message(chat_id=settings['autopost']['chatid'],
                text=ret_str,
                parse_mode=ParseMode.HTML)

def confirmed(context):
    total = vg.get_data('confirmed','total')
    newToday = vg.get_data('confirmed','newToday')
    last_diff = vg.get_last_diff('confirmed')
    timestr = get_timestr()

    if last_diff != 0:
        messagetext = get_messagetext('confirmed', last_diff)

        if last_diff < 0:
            ret_str = None
        else:
            ret_str =  "{} - &#129440; <b>{}</b> {}\n".format(timestr, last_diff, messagetext)
            ret_str += "{} - Totalt: <b>{}</b> (Nye i dag: <b>{}</b>)".format(timestr, total, newToday)

        vg.update_last_diff('confirmed')

        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=ret_str,
                        parse_mode=ParseMode.HTML)
    else:
        return None

def dead(context):
    total = vg.get_data('dead','total')
    newToday = vg.get_data('dead','newToday')
    last_diff = vg.get_last_diff('dead')
    timestr = get_timestr()

    if last_diff != 0:
        messagetext = get_messagetext('dead', last_diff)

        # If number is negative, convert to positive
        if last_diff < 0:
            last_diff = last_diff * -1

        vg.update_last_diff('dead')

        ret_str = "{} - &#10071; <b>{}</b> {}".format(timestr, last_diff, messagetext)
        ret_str += "\n{} - Totalt: <b>{}</b> (Nye i dag: <b>{}</b>)".format(timestr, total, newToday)

        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=ret_str,
                        parse_mode=ParseMode.HTML)
    else:
        return None

def hospitalized(context):
    total = vg.get_data('hospitalized','total')
    last_diff = vg.get_last_diff('hospitalized')
    timestr = get_timestr()

    if last_diff != 0:
        messagetext = get_messagetext('hospitalized', last_diff)

        # If number is negative, convert to positive
        if last_diff < 0:
            last_diff = last_diff * -1

        vg.update_last_diff('hospitalized')

        ret_str = "{} - &#127973; <b>{}</b> {}".format(timestr, last_diff, messagetext)
        ret_str += "\n{} - Totalt: <b>{}</b>".format(timestr, total)

        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=ret_str,
                        parse_mode=ParseMode.HTML)
    else:
        return None

def intensiveCare(context):
    total = vg.get_data('intensiveCare','total')
    last_diff = vg.get_last_diff('intensiveCare')
    timestr = get_timestr()

    if last_diff != 0:
        messagetext = get_messagetext('intensiveCare', last_diff)

        # If number is negative, convert to positive
        if last_diff < 0:
            last_diff = last_diff * -1

        vg.update_last_diff('intensiveCare')

        ret_str = "{} - 🤒 <b>{}</b> {}".format(timestr, last_diff, messagetext)
        ret_str += "\n{} - Totalt: <b>{}</b>".format(timestr, total)

        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=ret_str,
                        parse_mode=ParseMode.HTML)
    else:
        return None

def respiratory(context):
    total = vg.get_data('respiratory','total')
    last_diff = vg.get_last_diff('respiratory')
    timestr = get_timestr()

    if last_diff != 0:
        messagetext = get_messagetext('respiratory', last_diff)

        # If number is negative, convert to positive
        if last_diff < 0:
            last_diff = last_diff * -1

        vg.update_last_diff('respiratory')

        ret_str = "{} - 😷 <b>{}</b> {}".format(timestr, last_diff, messagetext)
        ret_str += "\n{} - Totalt: <b>{}</b>".format(timestr, total)

        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=ret_str,
                        parse_mode=ParseMode.HTML)
    else:
        return None

def quarantineEmployees(context):
    total = vg.get_data('quarantineEmployees','total')
    last_diff = vg.get_last_diff('quarantineEmployees')
    timestr = get_timestr()

    if last_diff != 0:
        messagetext = get_messagetext('quarantineEmployees', last_diff)

        # If number is negative, convert to positive
        if last_diff < 0:
            last_diff = last_diff * -1

        vg.update_last_diff('quarantineEmployees')

        ret_str = "{} - ☣️ <b>{}</b> {}".format(timestr, last_diff, messagetext)
        ret_str += "\n{} - Totalt: <b>{}</b>".format(timestr, total)

        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=ret_str,
                        parse_mode=ParseMode.HTML)
    else:
        return None

def infectedEmployees(context):
    total = vg.get_data('infectedEmployees','total')
    last_diff = vg.get_last_diff('infectedEmployees')
    timestr = get_timestr()

    if last_diff != 0:
        messagetext = get_messagetext('infectedEmployees', last_diff)

        if last_diff < 0:
            last_diff = last_diff * -1

        vg.update_last_diff('infectedEmployees')

        ret_str = "{} - &#129440;🧑‍⚕️ <b>{}</b> {}".format(timestr, last_diff, messagetext)
        ret_str += "\n{} - Totalt: <b>{}</b>".format(timestr, total)

        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=ret_str,
                        parse_mode=ParseMode.HTML)
    else:
        return None

def rss_fhi(context):
    res = rss.fhi()
    if res is not None:
        context.bot.send_message(chat_id=settings['autopost']['chatid'],
                        text=res,
                        parse_mode=ParseMode.HTML)

def tested_graph(context):
    context.bot.send_photo(chat_id=settings['autopost']['chatid'],
                photo=graphs.tested())

def confirmed_graph(context):
    context.bot.send_photo(chat_id=settings['autopost']['chatid'],
                photo=graphs.confirmed())

def dead_graph(context):
    context.bot.send_photo(chat_id=settings['autopost']['chatid'],
                photo=graphs.dead())

def hospitalized_graph(context):
    context.bot.send_photo(chat_id=settings['autopost']['chatid'],
                photo=graphs.hospitalized())

def nordic_confirmed_graph(context):
    context.bot.send_photo(chat_id='83045611',
                photo=graphs.nordic_confirmed(),
                caption='Antall smittede i Norge, Sverige, Danmark (per 100k innbygger)')

def nordic_dead_graph(context):
    context.bot.send_photo(chat_id='83045611',
                photo=graphs.nordic_dead(),
                caption='Antall døde i Norge, Sverige, Danmark (per 100k innbygger)')