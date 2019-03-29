# If modifying these scopes, delete the file token.json.

from gmailHandler import gmailHandler
from controller import controller
from TelegramAlerts import TelegramAlerts



SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():

    #  CHANGE THIS TO GO FROM TESTNET TO LIVENET
    real_money = True
    gmail = gmailHandler('credentials.json')

    telegramBot = TelegramAlerts(gmail)
    telegramBot.run()

    #TODO: figure out how to run both at the same time

    trader = controller(gmail, .001, .1, real_money)

    trader.importAPIKeys()
    trader.run()





if __name__ == '__main__':
    main()
