import sys
import yaml
from telegram import ParseMode

sys.path.append('./modules/')
from utils import get_messagetext, get_timestr, get_yesterday, grafana_seconds
from vg import VG
import grafana
import graphs

with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

settings = cfg['bot']
vg = VG()

def chatid(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                    text="Chatid: {}".format(update.message.chat_id),
                    parse_mode=ParseMode.HTML)

def help(update, context):
    menuitems = '<b>' + settings['commands']['title'] + '</b>\n'
    
    for command in list(settings['commands'].items())[1:]:
        menuitems += command[1] + '\n'

    context.bot.send_message(chat_id=update.message.chat_id,
                    text=menuitems,
                    parse_mode=ParseMode.HTML)

def stats(update, context):
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

    context.bot.send_message(chat_id=update.message.chat_id,
                text=ret_str,
                parse_mode=ParseMode.HTML)

def tested_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id,
        photo=graphs.tested())

def confirmed_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id,
                photo=graphs.confirmed())

def dead_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id,
                photo=graphs.dead())

def hospitalized_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id,
                photo=graphs.hospitalized())

def hospit_graph(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id,
                photo=graphs.hospitalized())
