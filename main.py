# If modifying these scopes, delete the file token.json.

from gmailHandler import gmailHandler
from controller import controller
from TelegramAlerts import TelegramAlerts
import threading


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():

    #  CHANGE THIS TO GO FROM TESTNET TO LIVENET
    real_money = True
    gmail = gmailHandler('credentials.json')

    telegramBot = TelegramAlerts(gmail)
    trader = controller(gmail, .001, .1, real_money)

    trader.importAPIKeys()

    threading.Thread(target=telegramBot.run).start()

    threading.Thread(target=trader.run).start()


if __name__ == '__main__':
    main()
