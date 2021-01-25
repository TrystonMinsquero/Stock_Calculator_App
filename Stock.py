import bs4
import requests


def get_price(tag):
    r = requests.get('https://finance.yahoo.com/quote/' + tag + '?p=' + tag + '&.tsrc=fin-srch')
    soup = bs4.BeautifulSoup(r.text, features='html.parser')
    if soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}) is not None:
        return float(soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text)
    else:
        raise Exception("Stock price can't be found")


def get_dividend(tag):
    def convert_div(text):
        div = ""
        if "(" in text:
            start = text.find("(") + 1
        else:
            start = 0
        stop = text.find("%")
        for i in range(start, stop):
            div += text[i]
        try:
            return float(div)
        except ValueError:
            return 0

    r = requests.get('https://finance.yahoo.com/quote/' + tag + '?p=' + tag + '&.tsrc=fin-srch')
    soup = bs4.BeautifulSoup(r.text, features='html.parser')
    for tableRow in soup.find('div', {'id': 'quote-summary'}).find_all('tr', {
        'class': 'Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)'}):
        if tableRow.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'}) is not None:
            return convert_div(tableRow.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'}).text)
        elif tableRow.find('td', {'data-test': 'TD_YIELD-value'}) is not None:
            return convert_div(tableRow.find('td', {'data-test': 'TD_YIELD-value'}).text)
    return 0


class Stock(object):

    def __init__(self, tag, current_price=0, div_yield=0):
        self.tag = tag
        self.current_price = current_price
        self.div_yield = div_yield

    def update(self):
        self.current_price = get_price(self.tag)
        self.div_yield = get_dividend(self.tag)

    def get_current_price(self, shares=1):
        return "$" + str(self.current_price * shares)

    def get_div_yield(self):
        return str(round(self.div_yield, 2)) + '%'

    def get_exp_yearly_yield(self, shares=1):
        return "$" + str(round(self.current_price*self.div_yield*shares/100, 2))

    def get_exp_quarterly_yield(self, shares=1):
        return "$" + str(round(self.current_price*self.div_yield*shares/400, 2))

    @str
    def __str__(self):
        return self.tag + " | $" + str(self.current_price) + " | " + str(round(self.div_yield, 2)) + '%'

    def print(self):
        print((self.tag + " | $" + str(self.current_price) + " | " + str(round(self.div_yield, 2)) + '%'))


