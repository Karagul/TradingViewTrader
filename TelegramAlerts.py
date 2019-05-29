#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''$$ billz yall'''

import telegram
from telegram import Bot
import logging
from time import sleep
from telethon import TelegramClient, events

from telethon import functions, types
from telethon.tl.functions.messages import GetHistoryRequest

update_id = None


class TelegramAlerts:

    gmailController = None
    channel = None
    telegramClient = None

    def __init__(self, gmailHandler):

        self.gmailController = gmailHandler


        '''Telegram api keys and channel name are hardcoded'''
        #TODO: put these in the api key file

        self.telegramClient = TelegramClient('kcapbot', '724640', '71b22453559c8403882e88f990be5c77')
        self.telegramClient.connect

        self.channel = self.telegramClient.get_entity('MCP_binance')    #this call uses the '@username' to to create an entity
                                                                    #TODO: get Tylers vip group name and see if we can hack in.



    def run(self):
        #
        # posts = telegramClient(GetHistoryRequest(
        #     peer=self.channel,
        #     limit=1,
        #     offset_date=None,
        #     offset_id=0,
        #     max_id=0,
        #     min_id=0,
        #     add_offset=0,
        #     hash=0))

        @self.telegramClient.on(events.NewMessage)
        async def my_event_handler(event):
            parseMessage(self, event.raw_text)

        self.telegramClient.start()


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