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
            count = 0

            try:
                self.getTradeData(self.bot)
                sleep(1)
                if count % 240 == 0:
                    print("\n")
                print("|", end="", flush=True)
                count = count + 1
            except python_telegram_bot_master.telegram.error.NetworkError:
                sleep(1)
            except python_telegram_bot_master.telegram.error.Unauthorized:
                # The user has removed or blocked the bot.
                update_id += 1


    def getTradeData(self, bot):
        """Grab the message parse the data and format for Gmail
        handler. subject looks like: '$$$ BUY BTC USD $$$' """
        takeGains = []

        global update_id
        # Request updates after the last update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1

            if update.message:  # your bot can receive updates without messages

                text = update.message.text
                alertIdentifiers = ["BUY", "Buy", "Entry", "ENTRY"]
                takeProfitIdentifiers = ["Tg","TG","Tp","TP"]

                if any(x in text for x in alertIdentifiers):

                        print("message:\n\n%s\n" % text)

                        lines = text.splitlines(False)
                        for line in lines:

                            if "#" in line:
                                coin = line[line.find("#")+1:]

                                if " " in line:
                                    coin = coin[:line.find(" ")]

                                print("Coin: " + coin + "\n")

                            if any(x in line for x in takeProfitIdentifiers):
                                takeProfit = line[line.find(" "):]

                                if " " in line:
                                    takeProfit = takeProfit[:line.find(" ")]

                                print("Take profit: " + takeProfit + "\n")
                                takeGains.append(takeProfit)



                        #TODO; add the money signs to subject when this is all figured out
                        #TODO: figure out coin pair for each trade

                        subject = ("$$ %s BTC LONG $$" % coin)
                        print(coin + "\n")
                        print(subject + "\n")

                        '''final determination of wether the alert is actually an alert.
                         if we have 1 or more take profit indicator'''
                        if len(takeGains) >= 1:
                            alert = self.gmailController.createMessage(subject, takeGains[0])
                            self.gmailController.sendEmail(alert)


