import requests
import shutil
import yaml
import os
from utils import grafana_seconds

with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

settings = cfg['grafana']['zomg']
graph_dir = settings['graph_dir']
headers = {'Authorization': 'Bearer ' + settings['token'] }

if not os.path.exists(graph_dir):
    os.makedirs(graph_dir)

def tested():
    url = settings['base'] + settings['tested']['url_start'] + grafana_seconds() + settings['tested']['url_end']
    res = requests.get(url, headers=headers, stream=True)
    local_file = open(graph_dir + 'tested.jpg', 'wb')
    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, local_file)
    del res
    return(
        open(graph_dir + 'tested.jpg', 'rb')
    )

def confirmed():
    url = settings['base'] + settings['confirmed']['url_start'] + grafana_seconds() + settings['confirmed']['url_end']
    res = requests.get(url, headers=headers, stream=True)
    local_file = open(graph_dir + 'confirmed.jpg', 'wb')
    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, local_file)
    del res
    return(
        open(graph_dir + 'confirmed.jpg', 'rb')
    )

def dead():
    url = settings['base'] + settings['dead']['url_start'] + grafana_seconds() + settings['dead']['url_end']
    res = requests.get(url, headers=headers, stream=True)
    local_file = open(graph_dir + 'dead.jpg', 'wb')
    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, local_file)
    del res
    return(
        open(graph_dir + 'dead.jpg', 'rb')
    )

def hospitalized():
    url = settings['base'] + settings['hospitalized']['url_start'] + grafana_seconds() + settings['hospitalized']['url_end']
    res = requests.get(url, headers=headers, stream=True)
    local_file = open(graph_dir + 'hospitalized.jpg', 'wb')
    res.raw.decode_content = True
    shutil.copyfileobj(res.raw, local_file)
    del res
    return(
        open(graph_dir + 'hospitalized.jpg', 'rb')
    )