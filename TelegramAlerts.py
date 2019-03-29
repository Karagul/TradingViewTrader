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

        print("Telegram Account authorized:\nListening for Alerts")
        while True:

            try:
                self.getTradeData(self.bot)
            except python_telegram_bot_master.telegram.error.NetworkError:
                sleep(1)
            except python_telegram_bot_master.telegram.error.Unauthorized:
                # The user has removed or blocked the bot.
                update_id += 1


    def getTradeData(self, bot):
        """Grab the message parse the data and format for Gmail
        handler. subject looks like: '$$$ BUY BTC USD $$$' """
        tgCount = 0

        global update_id
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1

            if update.message:  # your bot can receive updates without messages
                text = update.message.text
                if (("Buy" or "BUY" or "Entry" or "ENTRY") in text):

                        print("message:\n\n%s\n\n" % text)

                        for line in text:
                            if "#" in line:
                                coin = line[line.find("#"):]
                                coin = coin[:line.find(" ")]
                                print("Coin: " + coin + "")

                            if ("Tg" or "TG" or "Tp" or "TP") in line:
                                takeProfit = line[line.find("#"):]
                                takeProfit = takeProfit[:line.find(" ")]
                                print("Take profit: " + takeProfit + "\n")
                                tgCount += 1



                        #TODO; add the money signs to subject when this is all figured out
                        #TODO: figure out coin pair for each trade

                        subject = ("BUY %s BTC" % coin)
                        print(coin + "\n")
                        print(subject + "\n")

                        '''final determination of wether the alert is actually an alert.
                         if we have 2 or more take profit indicator'''
                        if tgCount > 1:
                            alert = self.gmailController.createMessage(subject, " ")
                            self.gmailController.sendEmail(alert)


