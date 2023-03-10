from redis_db import *

ex1 = [{
    'exchange': 'Binance',
    'coin': 'BNB',
    'free': '0.0280778',
    'node': {
        'symbol': 'BNBUSDT',
        'baseAsset': 'BNB',
        'quoteAsset': 'USDT'}},
    {'exchange': 'Gate.io',
     'coin': 'USDT',
     'free': '1000',
     'node': {'symbol': 'BNBUSDT',
              'baseAsset': 'BNB',
              'quoteAsset': 'USDT'}}]

PERCENT = 0.5


def compare_prices(bunch):
    node1 = bunch[0]['exchange'] + '_' + bunch[0]['node']['symbol']
    node2 = bunch[1]['exchange'] + '_' + bunch[1]['node']['symbol']
    bid1, ask1 = map(float, get_redis(node1).split(','))
    bid2, ask2 = map(float, get_redis(node2).split(','))

    print(node1)
    print(node2)
    print(bid1, ask1)
    print(bid2, ask2)
    print((bid2 - ask1) / bid2 * 100)
    print((bid1 - ask2) / bid1 * 100)
    if (bid2 - ask1) / bid2 * 100 > PERCENT:
        return 'BUY/SELL'
    if (bid1 - ask2) / bid1 * 100 > PERCENT:
        return 'SELL/BUY'

    return None
