import logging
import yaml
import sys
import os
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from datetime import datetime, timedelta

sys.path.append('./modules/')
from utils import wait_seconds, midnight_seconds, job_initiate, job_enable
import handlers
import jobs

with open('./config/config.yml', 'r') as ymlfile:
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
    for job in settings['autopost']['jobs']:
        try:
            exec(job_initiate(job))
            exec(job_enable(job))
        except:
            print('Error initiating job:', job)

    # Error handler
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()