# COVID-19 Norge - Telegram Bot
<a href="https://t.me/s/covid19norge">
<div align="center">
<img src="https://user-images.githubusercontent.com/11590359/83902735-38810c80-a75d-11ea-94f8-dbc6aff85a61.png"/>

<b>COVID-19 Norge</b> <br>
*(Preview)*
</div>
</a>

## Description
Telegram bot for tracking live COVID-19 statistics in Norway.

The bot autoposts live COVID-19 updates to a group/channel/user of your choosing:
```yaml
bot:
  token: BOT_TOKEN
  autopost:
    chatid: CHAT_ID
```

Bot is live in this channel: [COVID-19 Norge](https://t.me/s/covid19norge)

## Screenshots
#### Live Updates
<p align="left">
<img width=415 alt="c19_stats" src="https://user-images.githubusercontent.com/11590359/99575530-098fe780-29d9-11eb-9250-975274dbd8ce.png">
<img width=415 alt="c19_live" src="https://user-images.githubusercontent.com/11590359/99575184-92f2ea00-29d8-11eb-902c-597becc9c524.png">
</p>

#### Graphs
<p align="left">
<img width=415 alt="c19_graphs-1" src="https://user-images.githubusercontent.com/11590359/99575030-66d76900-29d8-11eb-9489-69a7988a10ef.png">
<img width=415 alt="c19_graphs-2" src="https://user-images.githubusercontent.com/11590359/99575102-78b90c00-29d8-11eb-80d8-2de2307a5ad4.png">
</p>

#### RSS
<p align="left">
 <img width=500 alt="c19_rss" src="https://user-images.githubusercontent.com/11590359/99575788-6095bc80-29d9-11eb-8e58-62b368c8e304.png">
</p>

## Features
### Autopost:

- **Live updates/events**
  - Tested
  - Confirmed cases
  - Deaths
  - Admissions
  - Respiratory
  - Vaccine doses
- **Graphs**
  - Tested
  - Confirmed
  - Dead
  - Hospitalized
  - Vaccine doses
- **RSS**
  - News from FHI (Folkehelseinstituttet)
  - News from the goverment (Regjeringen)

### Available functions:
- /help - Show commands
- /stats - COVID-19 statistikk Norge
- /tested - Graf over testede i Norge
- /confirmed - Graf over smittede i Norge
- /dead - Graf over dødsfall i Norge
- /hospitalized - Graf over sykehusinnleggelser i Norge
- /vaccine - Graf over antall personer vaksinert i Norge

## Installation

### Docker
##### Create a file named `docker-compose.yml` and add the following:
```yaml
version: '3.4'

services:
  bot:
    container_name: covid19norge-telegram-bot
    image: frefrik/covid19norge-telegram-bot
    restart: always
    environment:
      - TZ=Europe/Oslo
    volumes:
      - ./config:/app/bot/config
      - ./data:/app/bot/data
```

##### Download and edit bot configuration
```shell
$ mkdir -p config \
  && wget https://raw.githubusercontent.com/frefrik/covid19norge-telegram-bot/master/config/config.dist.yml -O config/config.yml
```

##### Start bot
```shell
$ docker-compose up -d
```

---
### git + Docker
##### Clone the repository
```shell
$ git clone https://github.com/frefrik/covid19norge-telegram-bot.git
$ cd covid19norge-telegram-bot/
```
##### Copy `config.dist.yml` to `config.yml` and edit configuration
```shell
$ cd config/
$ cp config.dist.yml config.yml
```

##### Start bot
```shell
$ docker-compose up -d
```

---

#### Docker Notes
##### Editing config
If `config.yaml` is updated while bot is running, the container must be restarted to use the updated config.
```shell
$ docker restart covid19norge-telegram-bot
```
##### Bot logs
Use `docker logs -f covid19norge-telegram-bot` to show informational logs.

---
### Command line
##### Install dependencies
```shell
$ pip install -r requirements.txt
```

##### Copy `config.dist.yml` to `config.yml` and edit configuration
```shell
$ cp config/config.dist.yml config/onfig.yml
```

##### Start bot
```shell
$ screen -dmS covid19norge python bot.py
```

##### Attaching to the screen
```shell
$ screen -r covid19norge
```

## Datasource
- [github.com/frefrik/c19norge-data](https://github.com/frefrik/c19norge-data) accessed through [c19norge.no/api](https://c19norge.no/api)
