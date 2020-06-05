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
#### Autopost Live Updates
<p align="left">
<img height=600 alt="c19_live" src="https://user-images.githubusercontent.com/11590359/83899631-11284080-a759-11ea-905f-6d96f7a90f25.png">
<img height=600 alt="c19_stats" src="https://user-images.githubusercontent.com/11590359/83899674-23a27a00-a759-11ea-8d9f-0129f2a0ae30.png">
</p>

#### Graphs
<p align="left">
<img height=500 alt="c19_graphs-1" src="https://user-images.githubusercontent.com/11590359/83899708-31f09600-a759-11ea-94a1-117cfcc3a324.png">
<img height=500 alt="c19_graphs-2" src="https://user-images.githubusercontent.com/11590359/83899716-33ba5980-a759-11ea-9c3c-0f5dbb0b2cc2.png">
</p>

#### RSS
<p align="left">
 <img width="497" alt="c19_rss" src="https://user-images.githubusercontent.com/11590359/83899729-387f0d80-a759-11ea-8f8b-b289e7a7cfc5.png">
</p>

## Features
### Autopost:

- **Live updates/events**
  - Tested
  - Confirmed/Infected
  - Dead
  - Hospitalized
  - Intensive Care
  - Respiratory
  - Quarantine Employees
  - Infected Employees
- **Graphs**
  - Tested
  - Confirmed/Infected
  - Dead
  - Hospitalized
  - Nordic Confirmed/Dead
- **RSS**
  - News from FHI (Folkehelseinstituttet)

### Available functions:
- /help - Show commands
- /stats - COVID-19 statistikk Norge
- /tested - Graf over testede i Norge
- /confirmed - Graf over smittede i Norge
- /dead - Graf over dødsfall i Norge
- /hospitalized - Graf over sykehusinnleggelser i Norge
- /n confirmed - Graf over antall smittede per 100k innb. i Norge, Sverige, Danmark
- /n dead - Graf over antall døde per 100k innb. i Norge, Sverige, Danmark
- /n hospitalized - Graf over antall innlagte per 100k innb. i Norge, Sverige, Danmark
- /ws \<country> - Country stats

## Installation
##### Install dependencies
```shell
pip install -r requirements.txt
```

## Configuration

##### 1. Rename `config.dist.yml` to `config.yml`
```shell
$ mv config.dist.yml config.yml
```

##### 2. Replace `BOT_TOKEN` with your Telegram BOT Token
```yaml
bot:
  token: BOT_TOKEN
```

##### 3. Replace `CHAT_ID` with the chatid where you want to enable autopost
```yaml
autopost:
  chatid: CHAT_ID
```

## Usage

##### Start bot
```shell
$ screen -dmS covid19norge python3 bot.py
```

##### Attaching to the screen
```shell
screen -r covid19norge
```

## Data Source
- https://www.vg.no/spesial/2020/corona/
