import os
from datetime import time
import logging
from telegram.ext import Updater, CommandHandler
from modules.utils import load_config, file_write
from modules.utils import job_initiate, job_enable, wait_seconds
import modules.c19api as c19api
import handlers
import jobs

cfg = load_config()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
bot = cfg["bot"]


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

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    check_files_exist()
    main()
