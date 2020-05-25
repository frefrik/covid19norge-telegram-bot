import logging
import yaml
import sys
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from datetime import datetime, timedelta

sys.path.append('./src/')
from c19_utils import wait_seconds, midnight_seconds
from c19_rss import RSS
import c19_grafana
import c19_stats

with open('./config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

settings = cfg['bot']

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

''' Command - Get chatid '''
def chatid(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                    text="Chatid: {}".format(update.message.chat_id),
                    parse_mode=ParseMode.HTML)

''' Command - Help '''
def help(update, context):
    menuitems = '<b>' + settings['commands']['title'] + '</b>\n'
    
    for command in list(settings['commands'].items())[1:]:
        menuitems += command[1] + '\n'

    context.bot.send_message(chat_id=update.message.chat_id,
                    text=menuitems,
                    parse_mode=ParseMode.HTML)

''' Error logging '''
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)

    if update.effective_message:
        text = "Hey. I'm sorry to inform you that an error happened while I tried to handle your update."
        update.effective_message.reply_text(text)

def main():
    stats_job = c19_stats.Job()
    stats_cmd = c19_stats.Command()
    grafana_job = c19_grafana.Job()
    grafana_cmd = c19_grafana.Command()
    rss = RSS()

    updater = Updater(settings['token'], use_context=True)
    dp = updater.dispatcher
    jq = updater.job_queue

    ''' Commands '''
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('chatid',chatid))
    dp.add_handler(CommandHandler('stats',stats_cmd.stats))
    dp.add_handler(CommandHandler('tested',grafana_cmd.tested))
    dp.add_handler(CommandHandler('confirmed',grafana_cmd.confirmed))
    dp.add_handler(CommandHandler('dead',grafana_cmd.dead))
    dp.add_handler(CommandHandler('hospitalized',grafana_cmd.hospitalized))
    
    ''' Jobs '''
    job_settings = settings['autopost']['jobs']

    j_rss = jq.run_repeating(rss.fhi, interval=job_settings['rss']['interval'] * 60, first=wait_seconds(job_settings['rss']['interval']))
    j_stats = jq.run_repeating(stats_job.stats, interval=job_settings['stats']['interval'] * 60, first=wait_seconds(job_settings['stats']['interval']))
    j_confirmed = jq.run_repeating(stats_job.confirmed, interval=job_settings['confirmed']['interval'] * 60, first=wait_seconds(job_settings['confirmed']['interval']))
    j_dead = jq.run_repeating(stats_job.dead, interval=job_settings['dead']['interval'] * 60, first=wait_seconds(job_settings['dead']['interval']))
    j_hospitalized = jq.run_repeating(stats_job.hospitalized, interval=job_settings['hospitalized']['interval'] * 60, first=wait_seconds(job_settings['hospitalized']['interval']))
    j_intensiveCare = jq.run_repeating(stats_job.intensiveCare, interval=job_settings['intensiveCare']['interval'] * 60, first=wait_seconds(job_settings['intensiveCare']['interval']))
    j_respiratory = jq.run_repeating(stats_job.respiratory, interval=job_settings['respiratory']['interval'] * 60, first=wait_seconds(job_settings['respiratory']['interval']))
    j_quarantineEmployees = jq.run_repeating(stats_job.quarantineEmployees, interval=job_settings['quarantineEmployees']['interval'] * 60, first=wait_seconds(job_settings['quarantineEmployees']['interval']))
    j_infectedEmployees = jq.run_repeating(stats_job.infectedEmployees, interval=job_settings['infectedEmployees']['interval'] * 60, first=wait_seconds(job_settings['infectedEmployees']['interval']))
    j_graph_tested = jq.run_repeating(grafana_job.tested, interval=job_settings['graph_tested']['interval'] * 60, first=midnight_seconds())
    j_graph_confirmed = jq.run_repeating(grafana_job.confirmed, interval=job_settings['graph_confirmed']['interval'] * 60, first=midnight_seconds())
    j_graph_dead = jq.run_repeating(grafana_job.dead, interval=job_settings['graph_dead']['interval'] * 60, first=midnight_seconds())
    j_graph_hospitalized = jq.run_repeating(grafana_job.hospitalized, interval=job_settings['graph_hospitalized']['interval'] * 60, first=midnight_seconds())
    
    ''' Enable jobs '''
    j_rss.enabled = job_settings['rss']['enabled']
    j_stats.enabled = job_settings['stats']['enabled']
    j_confirmed.enabled = job_settings['confirmed']['enabled']
    j_dead.enabled = job_settings['dead']['enabled']
    j_hospitalized.enabled = job_settings['hospitalized']['enabled']
    j_intensiveCare.enabled = job_settings['intensiveCare']['enabled']
    j_respiratory.enabled = job_settings['respiratory']['enabled']
    j_quarantineEmployees.enabled = job_settings['quarantineEmployees']['enabled']
    j_infectedEmployees.enabled = job_settings['infectedEmployees']['enabled']
    j_graph_tested.enabled = job_settings['graph_tested']['enabled']
    j_graph_confirmed.enabled = job_settings['graph_confirmed']['enabled']
    j_graph_dead.enabled = job_settings['graph_dead']['enabled']
    j_graph_hospitalized.enabled = job_settings['graph_hospitalized']['enabled']

    # Error handler
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()