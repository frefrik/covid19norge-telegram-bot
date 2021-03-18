import json
import yaml
from datetime import datetime, timedelta

with open("./config/config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


def get_messagetext(job, diff):
    job = cfg["bot"]["autopost"]["jobs"][job]

    if diff is None:
        return None
    if diff == 1:
        messagetext = job.get("text_pos_singular")
    elif diff > 1:
        messagetext = job.get("text_pos_plural")
    elif diff == -1:
        messagetext = job.get("text_neg_singular")
    elif diff < -1:
        messagetext = job.get("text_neg_plural")
    else:
        return None

    return messagetext


def get_timestr():
    timestr = datetime.now().strftime("%H:%M")

    return timestr


def wait_seconds(job):
    cfg = load_config()
    interval = cfg["bot"]["autopost"]["jobs"][job]["interval"]

    now = datetime.now()
    next = now + (datetime.min - now) % timedelta(minutes=int(interval))
    sec_wait = (next - now).seconds + 10

    return sec_wait


def midnight_seconds():
    now = datetime.now()
    midnight_delta = timedelta(days=1)
    midnight_next = (now + midnight_delta).replace(
        hour=0, minute=5, microsecond=0, second=0
    )
    next_midnight = (midnight_next - now).seconds

    return next_midnight


def job_initiate(job):
    jobs = cfg["bot"]["autopost"]["jobs"]

    if job in jobs:
        data = jobs[job]
        job_var = "j_" + job
        job_interval = data["interval"] * 60

        jq_run = f"{job_var} = jq.run_repeating(jobs.{job}, interval={job_interval}, first=wait_seconds('{job}'))"

        return jq_run
    else:
        return None


def job_enable(job):
    jobs = cfg["bot"]["autopost"]["jobs"]

    if job in jobs:
        job_var = "j_" + job
        job_enabled = jobs.get(job, {}).get("enabled")
        jq_enabled = f"{job_var}.enabled = {job_enabled}"

        return jq_enabled
    else:
        return None


def load_config():
    with open("./config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    return cfg


def file_open(category):
    return open(f"data/{category}.txt", "r").read()


def file_write(category, data):
    fh = open(f"data/{category}.txt", "w")
    fh.write(str(data))
    fh.close()


def file_open_json(category):
    with open(f"data/{category}.json") as json_file:
        data = json.load(json_file)

    return data


def file_write_json(category, data):
    with open(f"data/{category}.json", "w") as json_file:
        json.dump(data, json_file)
