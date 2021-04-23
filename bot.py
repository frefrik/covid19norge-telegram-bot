import os
import time
import html
import json
import logging
import traceback
from datetime import time
from telegram import ParseMode, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from modules.utils import load_config, file_write
from modules.utils import job_initiate, job_enable, wait_seconds
import modules.c19api as c19api
import handlers
import jobs

cfg = load_config()

logging.basicConfig(
    level=logging.WARN, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
bot = cfg["bot"]


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    context.bot.send_message(
        chat_id=bot["chatid_dev"], text=message, parse_mode=ParseMode.HTML
    )


def check_files_exist():
    filenames = ["tested", "confirmed", "dead", "admissions", "respiratory"]

    for filename in filenames:
        if os.path.isfile(f"./data/{filename}.txt"):
            pass
        else:
            print(f"datafile for {filename} missing. Creating file with latest data.")
            currentData = c19api.metadata(filename, "total")

            file_write(filename, currentData)


def main():
    updater = Updater(bot["token"], use_context=True)
    dp = updater.dispatcher
    jq = updater.job_queue

    # handlers
    commands = [
        ("help", handlers.help),
        ("chatid", handlers.chatid),
        ("stats", handlers.stats),
        ("tested", handlers.tested_graph),
        ("confirmed", handlers.confirmed_graph),
        ("dead", handlers.dead_graph),
        ("hospitalized", handlers.hospitalized_graph),
        ("smittestopp", handlers.smittestopp_graph),
        ("vaccine", handlers.vaccine_doses_graph),
    ]

    for (name, callback) in commands:
        dp.add_handler(CommandHandler(name, callback))

    # jobs
    for job in bot["autopost"]["jobs"]:
        try:
            exec(job_initiate(job))
            exec(job_enable(job))
        except Exception:
            print("Error initiating job:", job)
            raise

    jq.run_daily(jobs.stats, time(hour=22, minute=30))

    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    check_files_exist()
    main()
