from marketOrderMarket import marketOrderMarket


class Binance2(marketOrderMarket):
    def getCurrentPrice(self, asset, currency):
        pass

    def marketBuy(self, orderSize, asset, currency, note):
        pass

    def marketSell(self, orderSize, asset, currency, note):
        pass

    def connect(self):
        pass

    def getAmountOfItem(self, coin):
        pass

    def makeOrder(self, order):
        pass

    def interpretType(self, type):
        pass

    def getMaxAmountToUse(self, asset, currency):
        pass