#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''$$ billz yall'''
# from python_telegram_bot_master.telegram import Bot
import python_telegram_bot_master.telegram
import logging
from time import sleep


update_id = None


class TelegramAlerts:

    gmailController = None
    bot = None

    def __init__(self, gmailHandler):

        self.gmailController = gmailHandler

        global update_id
        # Telegram Bot Authorization Token
        self.bot = python_telegram_bot_master.telegram.Bot('814404627:fuxaznhaxers')


    def run(self):

        # get the first pending update_id, this is so we can skip over it in case
        # we get an "Unauthorized" exception.
        try:
            update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            update_id = None

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        while True:
            print("hi")
            try:
                self.getTradeData(self.bot)
            except python_telegram_bot_master.telegram.error.NetworkError:
                sleep(1)
            except python_telegram_bot_master.telegram.error.Unauthorized:
                # The user has removed or blocked the bot.
                update_id += 1


    def getTradeData(self, bot):
        """Grab the message if it starts with '#'
        parse the data and format for Gmail handler.
        subject looks like: '$$$ BUY BTC USD $$$' """

        global update_id
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1

            if update.message:  # your bot can receive updates without messages
                if update.message.text.startswith('#'):
                    print("message starts with '#' ")
                    data = update.message.text.split("\n")
                    coin = data[0][1:]
                    tg1 = data[1]
                    tg2 = data[2]
                    tg3 = data[3]
                    stopLoss = data[4]
                    self.gmailController.sendEmail("hi")


