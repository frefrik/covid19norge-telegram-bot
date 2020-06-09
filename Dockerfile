FROM python:3.7-buster

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
RUN npm -g config set user root \
 && npm install -g canvas \
 && npm install -g vega vega-lite vega-cli

WORKDIR /app/bot
ADD . /app/bot
RUN mkdir -p graphs data

CMD ["python", "bot.py"]