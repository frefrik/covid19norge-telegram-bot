import requests
import shutil
import yaml
import os
from c19_utils import grafana_seconds

with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

class Data():
    def __init__(self):
        self.settings = cfg['grafana']['zomg']
        self.graph_dir = self.settings['graph_dir']
        self.headers = {'Authorization': 'Bearer ' + self.settings['token'] }

        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)

    def tested(self):
        url = self.settings['base'] + self.settings['tested']['url_start'] + grafana_seconds() + self.settings['tested']['url_end']
        res = requests.get(url, headers=self.headers, stream=True)
        local_file = open(self.graph_dir + 'tested.jpg', 'wb')
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, local_file)
        del res
        return(
            open(self.graph_dir + 'tested.jpg', 'rb')
        )

    def confirmed(self):
        url = self.settings['base'] + self.settings['confirmed']['url_start'] + grafana_seconds() + self.settings['confirmed']['url_end']
        res = requests.get(url, headers=self.headers, stream=True)
        local_file = open(self.graph_dir + 'confirmed.jpg', 'wb')
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, local_file)
        del res
        return(
            open(self.graph_dir + 'confirmed.jpg', 'rb')
        )

    def dead(self):
        url = self.settings['base'] + self.settings['dead']['url_start'] + grafana_seconds() + self.settings['dead']['url_end']
        res = requests.get(url, headers=self.headers, stream=True)
        local_file = open(self.graph_dir + 'dead.jpg', 'wb')
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, local_file)
        del res
        return(
            open(self.graph_dir + 'dead.jpg', 'rb')
        )

    def hospitalized(self):
        url = self.settings['base'] + self.settings['hospitalized']['url_start'] + grafana_seconds() + self.settings['hospitalized']['url_end']
        res = requests.get(url, headers=self.headers, stream=True)
        local_file = open(self.graph_dir + 'hospitalized.jpg', 'wb')
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, local_file)
        del res
        return(
            open(self.graph_dir + 'hospitalized.jpg', 'rb')
        )

class Command():
    def __init__(self):
        self.data = Data()

    def tested(self, update, context):
        context.bot.send_photo(chat_id=update.message.chat_id,
            photo=self.data.tested())

    def confirmed(self, update, context):
        context.bot.send_photo(chat_id=update.message.chat_id,
                    photo=self.data.confirmed())

    def dead(self, update, context):
        context.bot.send_photo(chat_id=update.message.chat_id,
                    photo=self.data.dead())

    def hospitalized(self, update, context):
        context.bot.send_photo(chat_id=update.message.chat_id,
                    photo=self.data.hospitalized())

class Job():
    def __init__(self):
        self.data = Data()
        self.settings = cfg['bot']['autopost']

    def tested(self, context):
        context.bot.send_photo(chat_id=self.settings['chatid'],
                    photo=self.data.tested())

    def confirmed(self, context):
        context.bot.send_photo(chat_id=self.settings['chatid'],
                    photo=self.data.confirmed())

    def dead(self, context):
        context.bot.send_photo(chat_id=self.settings['chatid'],
                    photo=self.data.dead())

    def hospitalized(self, context):
        context.bot.send_photo(chat_id=self.settings['chatid'],
                    photo=self.data.hospitalized())