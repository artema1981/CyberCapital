# from .redis_db import get_redis
# from models import DEMO_Trades
import redis
import json
from account.models import Profile
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
    PERCENT = 0.0
    MIN_USD_PICE = 20

    def __init__(self, bunch, user_pk):
        # general
        self.bunch = bunch
        self.user_pk = user_pk
        self.base_coin = bunch[0]['node']['baseAsset']
        self.quot_coin = bunch[0]['node']['quoteAsset']
        self.symbol = bunch[0]['node']['symbol']
        # node_1
        self.exchange1 = bunch[0]['exchange']
        self.free1 = float(bunch[0]['free'])
        self.coin1 = bunch[0]['coin']
        self.bid1, self.ask1 = None, None
        # node_2
        self.exchange2 = bunch[1]['exchange']
        self.free2 = float(bunch[1]['free'])
        self.coin2 = bunch[1]['coin']
        self.bid2, self.ask2 = None, None
        # print(json.loads(Profile.objects.get(user=self.user_pk).bio))
        # self.side = self.compare_prices()



    def update_bids_asks(self):
        if get_redis(f'{self.exchange1}_{self.symbol}') and get_redis(f'{self.exchange2}_{self.symbol}'):
            self.bid1, self.ask1 = map(float, get_redis(f'{self.exchange1}_{self.symbol}').split(','))
            self.bid2, self.ask2 = map(float, get_redis(f'{self.exchange2}_{self.symbol}').split(','))



    def max_quantity(self, side):
        if side == 'BUY/SELL':
            print([self.free1 / self.ask1, self.free2])
            res = sorted([self.free1 / self.ask1, self.free2])
            print(res)
            return res[0]


        # if (self.free1 * self.bid1) > self.free2:
        #     return round(self.free2/self.ask2, 6)
        # else:
        #     return self.free1

    def update_balance_dict(self, side, quantity):
        balances_dict = json.loads(Profile.objects.get(user=self.user_pk).bio)
        if side == 'BUY/SELL':

            print(balances_dict[self.exchange1][self.base_coin], '=', str(quantity), '+',
                  float(balances_dict[self.exchange1].get(self.base_coin, 0)))
            balances_dict[self.exchange1][self.base_coin] = str(round(
                float(quantity) + float(balances_dict[self.exchange1].get(self.base_coin, 0)), 6))

            print(balances_dict[self.exchange1][self.quot_coin], '=', balances_dict[self.exchange1].get(self.quot_coin),
                  '-', str(quantity), '*', self.ask1)
            balances_dict[self.exchange1][self.quot_coin] = str(round(
                float(balances_dict[self.exchange1].get(self.quot_coin)) - float(quantity)*self.ask1, 6))

            print(balances_dict[self.exchange2][self.base_coin], '=', balances_dict[self.exchange2][self.base_coin],
                  '-', float(quantity))
            balances_dict[self.exchange2][self.base_coin] = str(round(
                float(balances_dict[self.exchange2][self.base_coin]) - float(quantity), 6))

            print(balances_dict[self.exchange2][self.quot_coin], '=', float(balances_dict[self.exchange2].get(self.quot_coin, 0)), '+', float(quantity), '*', self.bid2)
            balances_dict[self.exchange2][self.quot_coin] = str(round(
                float(balances_dict[self.exchange2].get(self.quot_coin, 0)) + float(quantity)*self.bid2, 6))


            print(balances_dict)
        if side == 'SELL/BUY':
            balances_dict[self.exchange1][self.base_coin] = str(
                 float(balances_dict[self.exchange1].get(self.base_coin - float(quantity))))
            balances_dict[self.exchange1][self.quot_coin] = str(
                float(balances_dict[self.exchange1].get(self.quot_coin)) + float(quantity) * self.bid1)

            balances_dict[self.exchange2][self.base_coin] = str(
                float(balances_dict[self.exchange2].get(self.base_coin, 0) + float(quantity)))
            balances_dict[self.exchange2][self.quot_coin] = str(
                float(balances_dict[self.exchange1].get(self.quot_coin, 0)) - float(quantity) * self.ask2)

        prof_obj = Profile.objects.get(user=self.user_pk)
        prof_obj.bio = json.dumps(balances_dict, indent=2)
        prof_obj.save()


    def demo_trade(self, side, quantity):
        if side == 'BUY/SELL' and quantity > 0:

            profit = quantity * self.bid2 - quantity*self.ask1
            trade = {'BUY': {'exchange': f'{self.exchange1}',
                             'coin': f'{self.base_coin}',
                             'quantity': quantity,
                             'price': self.ask1},
                     'SELL':{'exchange': f'{self.exchange2}',
                             'coin': f'{self.base_coin}',
                             'quantity': quantity,
                             'price': self.bid2}
                     }

            print('*************BUY/SELL***********************')

            print(quantity)
            print(self.user_pk)
            print(str(profit))
            print(self.bunch)
            print(trade)
            print('********************************************')
            DEMO_Trades.objects.create(user =self.user_pk, bunch=self.bunch, trade=trade, profit=profit)
            self.update_balance_dict(side, quantity)


        if side == 'SELL/BUY' and quantity > 0:

            profit = quantity * self.bid1 - quantity * self.ask2
            trade = {'SELL': {'exchange': f'{self.exchange1}',
                             'coin': f'{self.base_coin}',
                             'quantity': quantity,
                             'price': self.bid1},
                     'BUY': {'exchange': f'{self.exchange2}',
                              'coin': f'{self.base_coin}',
                              'quantity': quantity,
                              'price': self.ask2}
                     }

            print('*************SELL/BUY***********************')
            print(quantity)
            print(self.user_pk)
            print(profit)
            print(self.bunch)
            print(trade)
            print('********************************************')
            DEMO_Trades.objects.create(user=self.user_pk, bunch=self.bunch, trade=trade, profit=profit)


    def compare_prices(self):
        self.update_bids_asks()

        if get_redis(f'{self.exchange1}_{self.symbol}') and get_redis(f'{self.exchange2}_{self.symbol}'):

            if (self.bid2 - self.ask1) / self.bid2 * 100 > Bunches.PERCENT and self.coin1 != self.base_coin and self.max_quantity('BUY/SELL')>0:
                print(self.bid2, self.ask1, self.coin1, self.base_coin, self.max_quantity('BUY/SELL'))

                self.demo_trade('BUY/SELL', self.max_quantity('BUY/SELL'))

            #
            # if (self.bid1 - self.ask2) / self.bid1 * 100 > Bunches.PERCENT and self.coin1 == self.base_coin:
            #
            #     self.demo_trade('SELL/BUY')






class_bunch_list = []
def create_bunch_class(user):
    decode = decode_js()
    if isinstance(decode, list):
        for i in decode:
            class_bunch_list.append(Bunches(i, user))

        # while True:
        for i in class_bunch_list:
            i.compare_prices()



