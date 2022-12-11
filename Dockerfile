FROM python:3.10-alpine3.17

MAINTAINER AlZa2022

COPY ./requirements.txt /dir-bot/requirements.txt

WORKDIR /dir-bot

RUN pip3 install -r requirements.txt

ENV serv_addr=""

ENV bot_token=""

ENV chat_bot_id=""

COPY ./aiogrammm /dir-bot

CMD exec python aio_bot.py $serv_addr $chat_bot_id $bot_token
