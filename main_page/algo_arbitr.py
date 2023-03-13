# from .redis_db import get_redis
# from models import DEMO_Trades
import redis
import json

from main_page.models import DEMO_Trades

redis_client = redis.Redis(host='localhost', port=6379, db=0)
def get_redis(name):
    try:
        volume = redis_client.get(name).decode('utf-8')

    except:
        volume = False

    return volume


def decode_js():
    if get_redis('bunches_list'):
        return json.loads(get_redis('bunches_list'))
    else:
        return 'error', get_redis('bunches_list')


class Bunches:
    PERCENT = 0.5
    MIN_USD_PICE = 20

    def __init__(self, bunch, user_pk):

        self.bunch = bunch
        self.user_pk = user_pk
        self.base_coin = bunch[0]['coin']
        self.base_exchange = bunch[0]['exchange']
        self.base_free = float(bunch[0]['free'])
        self.symbol = bunch[0]['node']['symbol']
        self.quot_coin = bunch[1]['coin']
        self.quot_exchange = bunch[1]['exchange']
        self.quot_free = float(bunch[1]['free'])
        self.base_bid, self.base_ask = None, None# map(float, get_redis(f'{self.base_exchange}_{self.symbol}').split(','))
        self.quot_bid, self.quot_ask = None, None#map(float, get_redis(f'{self.quot_exchange}_{self.symbol}').split(','))
        # self.update_bids_asks()
        self.side = self.compare_prices()



    def update_bids_asks(self):
        if get_redis(f'{self.base_exchange}_{self.symbol}') and get_redis(f'{self.quot_exchange}_{self.symbol}'):
            self.base_bid, self.base_ask = map(float, get_redis(f'{self.base_exchange}_{self.symbol}').split(','))
            self.quot_bid, self.quot_ask = map(float, get_redis(f'{self.quot_exchange}_{self.symbol}').split(','))




    def compare_prices(self):
        self.update_bids_asks()
        if get_redis(f'{self.base_exchange}_{self.symbol}') and get_redis(f'{self.quot_exchange}_{self.symbol}'):

            if (self.quot_bid - self.base_ask) / self.quot_bid * 100 > Bunches.PERCENT:
                # print(self.quot_bid, self.base_ask, (self.quot_bid - self.base_ask) / self.quot_bid * 100 )
                return 'BUY/SELL'
            if (self.base_bid - self.quot_ask) / self.base_bid * 100 > Bunches.PERCENT:
                # print(self.base_bid, self.quot_ask, (self.base_bid - self.quot_ask) / self.base_bid * 100)
                return 'SELL/BUY'

        return None

    def max_quantity(self):
        if (self.base_free * self.base_bid) > self.quot_free:
            return self.quot_free/self.quot_ask
        else:
            return self.base_free


    def demo_trade(self):
        quantity = self.max_quantity()
        if self.side == 'BUY/SELL':
            profit = quantity*self.quot_bid - quantity*self.base_ask
            trade = {'BUY': {'exchange': f'{self.base_exchange}',
                             'coin': f'{self.base_coin}',
                             'quantity': quantity,
                             'price': self.base_ask},
                     'SELL':{'exchange': f'{self.quot_exchange}',
                             'coin': f'{self.base_coin}',
                             'quantity': quantity,
                             'price': self.quot_bid}
                     }

            print('*************BUY/SELL***********************')

            print(quantity)
            print(self.user_pk)
            print(profit)
            print(self.bunch)
            print(trade)
            print('********************************************')
            DEMO_Trades.objects.create(user =self.user_pk, bunch=self.bunch, trade=trade, profit=profit)


        if self.side == 'SELL/BUY':

            profit = quantity * self.base_bid - quantity * self.quot_ask
            trade = {'SELL': {'exchange': f'{self.base_exchange}',
                             'coin': f'{self.base_coin}',
                             'quantity': quantity,
                             'price': self.base_bid},
                     'BUY': {'exchange': f'{self.quot_exchange}',
                              'coin': f'{self.base_coin}',
                              'quantity': quantity,
                              'price': self.quot_ask}
                     }

            print('*************SELL/BUY***********************')
            print(quantity)
            print(self.user_pk)
            print(profit)
            print(self.bunch)
            print(trade)
            print('********************************************')
            DEMO_Trades.objects.create(user=self.user_pk, bunch=self.bunch, trade=trade, profit=profit)


class_bunch_list = []
def create_bunch_class(user):
    decode = decode_js()
    if isinstance(decode, list):
        for i in decode:
            class_bunch_list.append(Bunches(i, user))

        x=class_bunch_list[-1]
        print(x.__dict__)


        # while True:
        for i in class_bunch_list:
            if i.side != None:
                i.demo_trade()
        print('cycle')
