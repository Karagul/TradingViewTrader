'''Alexander McKee'''
'''Class for listening to Telegram chat messages and parsing for email alerts'''

from telethon.sync import TelegramClient
from telethon import events


class TelegramAlerts:

    gmailController = None
    channel = None
    telegramClient = None
    message = None
    api_id = '724640'
    api_hash = '71b22453559c8403882e88f990be5c77'


    def __init__(self, gmailHandler):

        self.gmailController = gmailHandler


        with TelegramClient('name', self.api_id, self.api_hash) as client:
            self.telegramClient = client
            client.send_message('me', 'New Telegram bot created, listening for alerts...')
            print('Telegram account authorized')

            self.message = self.run()



    def run(self):
        @self.telegramClient.on(events.NewMessage())
        async def listen(event):
            message = await event.get_chat()
            print(message)
            return message

        self.telegramClient.run_until_disconnected()



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