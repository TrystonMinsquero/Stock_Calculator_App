from Stock import Stock
import os


class Profile(object):
    def __init__(self, name, stocksFile="list.txt", dataFile="data.txt"):
        self.name = name
        self.stocksFilePath = "profiles/" + name + "/" + stocksFile
        self.dataFilePath = "profiles/" + name + "/" + dataFile
        self.__read_stocks()
        self.__read_data()

    def get_total_current_prices(self):
        total = 0
        for stock in self.stocks:
            total += stock.current_price * self.stocks[stock]
        return "$" + str(round(total, 2))

    def get_total_yearly_dividend(self):
        total = 0
        for stock in self.stocks:
            total += round(stock.current_price*stock.div_yield*self.stocks[stock]/100, 2)
        return "$" + str(round(total, 2))

    def get_total_quarterly_dividend(self):
        total = 0
        for stock in self.stocks:
            total += round(stock.current_price*stock.div_yield*self.stocks[stock]/400, 2)
        return "$" + str(round(total, 2))

    def print_data(self):
        for attribute in self.data:
            print(attribute + ": " + str(self.data[attribute]))

    def print_stocks(self):
        for stock in self.stocks:
            print(stock.tag + ": " + str(self.stocks[stock]))

    def add_stock(self, stockTag, shares=1):
        stockFound = None
        stockTag = str(stockTag).upper()
        for stock in self.stocks:
            if stock.tag == stockTag:
                stockFound = stock

        if stockFound is None:
            self.stocks[Stock(stockTag)] = shares
            stocksFile = open(self.stocksFilePath, "a")
            stocksFile.write(stockTag + "=" + str(shares) + "\n")
            stocksFile.close()
        else:
            self.stocks[stockFound] = self.stocks[stockFound] + shares
            stocksFile = open(self.stocksFilePath)
            stocks = stocksFile.read()
            stocksFile.close()
            stocks = stocks.replace(stockTag + "=" + str(self.stocks[stockFound] - shares), stockTag + "=" + str(shares))
            stocksFile = open(self.stocksFilePath, "w")
            stocksFile.write(stocks)
            stocksFile.close()

    def edit_stock(self, stock, newShares):
        if newShares < 0:
            self.delete_stock(stock)
        stockFound = None
        for stock2 in self.stocks:
            if stock == stock2:
                stockFound = stock
        if stockFound is None:
            raise Exception("Stock not found")
        else:
            stocksFile = open(self.stocksFilePath)
            stocks = stocksFile.read()
            stocksFile.close()
            stocks = stocks.replace(stock.tag + "=" + str(self.stocks[stockFound]), stock.tag + "=" + str(newShares))
            self.stocks[stockFound] = newShares
            stocksFile = open(self.stocksFilePath, "w")
            stocksFile.write(stocks)
            stocksFile.close()

    def delete_stock(self, stock):
        stocksFile = open(self.stocksFilePath)
        stocks = stocksFile.read()
        stocksFile.close()
        if stock.tag in stocks:
            stocks = stocks.replace(stock.tag + "=" + str(self.stocks[stock]) + "\n", "")
        else:
            raise Exception("Stock not found")
        stocksFile = open(self.stocksFilePath, "w")
        stocksFile.write(stocks)
        stocksFile.close()
        self.stocks.pop(stock)

    def __read_stocks(self):
        stocks: dict[Stock, int]
        stocks = dict()
        try:
            stocksFile = open(self.stocksFilePath, "r")
            for line in stocksFile:
                line = line.split("=")
                stocks[Stock(line[0])] = int(line[1])
            stocksFile.close()
        except FileNotFoundError:
            open(self.stocksFilePath, "x")

        self.stocks = stocks

    def __read_data(self):
        data: dict[str, int]
        data = dict()
        try:
            dataFile = open(self.dataFilePath, "r")
            for line in dataFile:
                line = line.split("=")
                data[line[0]] = int(line[1])
            dataFile.close()
        except FileNotFoundError:
            open(self.dataFilePath, "x")

        self.data = data


# Will return true if successfully created directory for profile name and false if already exists
def create_profile_directory(name):
    try:
        os.mkdir("profiles/" + name)
        return True
    except FileExistsError:
        return False
