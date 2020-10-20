FROM python:3.8-slim

RUN apt update
RUN apt upgrade -y
RUN apt-get install vim -y
RUN apt-get install git -y

WORKDIR /dnd_discord_bot

EXPOSE 6543