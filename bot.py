import logging
import yaml
import sys
import os
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from datetime import datetime, timedelta

sys.path.append('./modules/')
from utils import wait_seconds, midnight_seconds
import handlers
import jobs

with open('./config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

if not os.path.exists('./graphs/'):
    os.makedirs('./graphs/')

settings = cfg['bot']

''' Error logging '''
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)

    if update.effective_message:
        text = "Hey. I'm sorry to inform you that an error happened while I tried to handle your update."
        update.effective_message.reply_text(text)
    
    raise

def main():
    updater = Updater(settings['token'], use_context=True)
    dp = updater.dispatcher
    jq = updater.job_queue

    ''' Commands '''
    commands = [('help', handlers.help),
                ('chatid', handlers.chatid),
                ('stats', handlers.stats),
                ('tested', handlers.tested_graph),
                ('confirmed', handlers.confirmed_graph),
                ('dead', handlers.dead_graph),
                ('hospitalized', handlers.hospitalized_graph),
                ('n',handlers.nordic_graph)]

    for (name, callback) in commands:
        dp.add_handler(CommandHandler(name, callback))

    ''' Jobs '''
    job_settings = settings['autopost']['jobs']

    j_rss = jq.run_repeating(jobs.rss_fhi, interval=job_settings['rss']['interval'] * 60, first=wait_seconds(job_settings['rss']['interval']))
    j_stats = jq.run_repeating(jobs.stats, interval=job_settings['stats']['interval'] * 60, first=wait_seconds(job_settings['stats']['interval']))
    j_confirmed = jq.run_repeating(jobs.confirmed, interval=job_settings['confirmed']['interval'] * 60, first=wait_seconds(job_settings['confirmed']['interval']))
    j_dead = jq.run_repeating(jobs.dead, interval=job_settings['dead']['interval'] * 60, first=wait_seconds(job_settings['dead']['interval']))
    j_hospitalized = jq.run_repeating(jobs.hospitalized, interval=job_settings['hospitalized']['interval'] * 60, first=wait_seconds(job_settings['hospitalized']['interval']))
    j_intensiveCare = jq.run_repeating(jobs.intensiveCare, interval=job_settings['intensiveCare']['interval'] * 60, first=wait_seconds(job_settings['intensiveCare']['interval']))
    j_respiratory = jq.run_repeating(jobs.respiratory, interval=job_settings['respiratory']['interval'] * 60, first=wait_seconds(job_settings['respiratory']['interval']))
    j_quarantineEmployees = jq.run_repeating(jobs.quarantineEmployees, interval=job_settings['quarantineEmployees']['interval'] * 60, first=wait_seconds(job_settings['quarantineEmployees']['interval']))
    j_infectedEmployees = jq.run_repeating(jobs.infectedEmployees, interval=job_settings['infectedEmployees']['interval'] * 60, first=wait_seconds(job_settings['infectedEmployees']['interval']))
    j_graph_tested = jq.run_repeating(jobs.tested_graph, interval=job_settings['graph_tested']['interval'] * 60, first=midnight_seconds())
    j_graph_confirmed = jq.run_repeating(jobs.confirmed_graph, interval=job_settings['graph_confirmed']['interval'] * 60, first=midnight_seconds())
    j_graph_dead = jq.run_repeating(jobs.dead_graph, interval=job_settings['graph_dead']['interval'] * 60, first=midnight_seconds())
    j_graph_hospitalized = jq.run_repeating(jobs.hospitalized_graph, interval=job_settings['graph_hospitalized']['interval'] * 60, first=midnight_seconds())
    
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