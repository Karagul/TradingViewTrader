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
        self.bot = python_telegram_bot_master.telegram.Bot('814404627:AAE1cxiFDJdvnXD2bUloSyBh3r603j4mGKg')


    def run(self):

        # get the first pending update_id, this is so we can skip over it in case
        # we get an "Unauthorized" exception.
        try:
            update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            update_id = None

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        print("Telegram Account authorized:\nListening for Alerts\n\n")
        while True:

            try:
                self.getTradeData(self.bot)
                sleep(3)

            except python_telegram_bot_master.telegram.error.NetworkError:
                sleep(1)
            except python_telegram_bot_master.telegram.error.Unauthorized:
                # The user has removed or blocked the bot.
                update_id += 1


    def getTradeData(self, bot):
        global update_id
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1

            if update.channel_post is not None:
                self.parseMessage(update.message.channel_post)

            if update.message and update.message.text is not None:  # your bot can receive updates without messages
                self.parseMessage(update.message.text)



    def parseMessage(self, text):
        """Grab the message parse the data and format for Gmail
        handler. subject looks like: '$$$ BUY BTC USD $$$' """

        takeGains = []
        alertIdentifiers = ["BUY", "Buy", "Entry", "ENTRY"]
        takeProfitIdentifiers = ["Tg", "TG", "Tp", "TP"]

        if any(x in text for x in alertIdentifiers):

            print("message:\n\n%s\n" % text)

            lines = text.splitlines(False)
            for line in lines:

                if "#" in line:
                    coin = line[line.find("#") + 1:]

                    if " " in line:
                        coin = coin[:line.find(" ")]

                    print("Coin: " + coin + "\n")

                if any(x in line for x in takeProfitIdentifiers):
                    takeProfit = line[line.find(" "):]

                    if " " in line:
                        takeProfit = takeProfit[:line.find(" ")]

                    print("Take profit: " + takeProfit + "\n")
                    takeGains.append(takeProfit)

                subject = ("$$ %s BTC LONG BINANCE $$" % coin.upper())
                print(coin + "\n" + subject + "\n")

            '''final determination of whether the alert is actually an alert.
             if we have 2 or more take profit indicators'''
            if len(takeGains) >= 2:
                alert = self.gmailController.createMessage(subject, takeGains[0])
                self.gmailController.sendEmail(alert)