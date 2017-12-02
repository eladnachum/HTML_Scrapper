class VirtualCoinPrice(object):
    """
    Class for virtual coin price data for a specific date (day)
    Attributes:
        price: virtual coin price for a specific date (day)
        open: open price
        high: high price
        low: low price
        date:
        change: change from previous day in percentage
    """

    def __init__(self,date,price,open=None,high=None,low=None,change=None):
        self.date = date
        self.price = float(price.replace(',',''))
        self.open = float(open.replace(',',''))
        self.high = float(high.replace(',',''))
        self.low = float(low.replace(',',''))
        self.change = float(change.strip('%'))

    def init_with_dict(self,data):
        self.date = data['date']
        self.price = data['price']
        self.open = data['open']
        self.high = data['high']
        self.low = data['low']
        self.change =  data['change']

    def calculate_change (self, last_day_price):
        if self.price:
            self.change = (self.price - last_day_price)/last_day_price
            return self.change
        else: return None

