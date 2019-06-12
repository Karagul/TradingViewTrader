# If modifying these scopes, delete the file token.json.
from gmailHandler import gmailHandler
from controller import controller
from TelegramAlerts import TelegramAlerts
from time import sleep
import threading


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():

    #  CHANGE THIS TO GO FROM TESTNET TO LIVENET
    count = 0
    real_money = False
    gmail = gmailHandler('credentials.json')

    trader = controller(gmail, .001, .1, real_money)
    trader.importAPIKeys()

    traderThread = threading.Thread(target=trader.run).start()

    telegramBot = TelegramAlerts(gmail)
    telegramThread = threading.Thread(target=telegramBot.run).start()


    while True:
        try:
            activeThreads = threading.enumerate()

            if threading.active_count() < 6 and activeThreads.__contains__(telegramThread):
                traderThread.start()

            elif activeThreads.__contains__(traderThread):
                telegramThread.start()
            else:

                if count % 180 == 0:
                    print("\n")
                print(".", end="", flush=True)
                count = count + 1
                sleep(1)

        except Exception as e:
            print(e)




if __name__ == '__main__':
    main()
