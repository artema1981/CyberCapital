from asgiref.sync import async_to_sync
from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
from .redis_db import *
from pybit import spot
import threading
import asyncio
from gate_ws import Configuration, Connection, WebSocketResponse
from gate_ws.spot import SpotPublicTradeChannel, SpotBookTickerChannel


#########____binance websocket____#################
def message_handler(message):
    if message.get('stream'):
        symbol = 'binance_' + message['data'].get('s')
        bid = message['data'].get('b')
        ask = message['data'].get('a')
        bidask = f'{bid},{ask}'
        print(symbol, bidask)
        set_redis(name=symbol, value=bidask)


my_client = Client()
my_client.start()



def run_websocket_binance(lst):
    my_client.book_ticker(
        symbol=lst,
        id=1,
        callback=message_handler,
    )


#########___bybit websocket___#################

def handle_orderbook(message):
    data = message["data"]
    symbol = 'bybit_' + data['s']
    bid = data['b'][0][0]
    ask = data['a'][0][0]
    bidask = f'{bid},{ask}'
    print(symbol, bidask)
    set_redis(name=symbol, value=bidask)


#
def ws_bybit(symbols):
    for i in symbols:
        ws_spot = spot.WebSocket(test=False)
        ws_spot.depth_v2_stream(handle_orderbook, i)


#########___Gate.Io websocket___#################

def print_message(conn: Connection, response: WebSocketResponse):
    # print(response.result)
    if response.error:
        print('error returned: ', response.error)
        conn.close()
        return

    data = response.result
    if not data.get('status'):
        symbol = 'gateio_' + ''.join(data.get('s').split('_'))
        bid = data.get('b')
        ask = data.get('a')
        bidask = f'{bid},{ask}'
        print(symbol, bidask)
        set_redis(name=symbol, value=bidask)



@async_to_sync
async def ws_gateio(symbols):
    # initialize default connection, which connects to spot WebSocket V4
    # it is recommended to use one conn to initialize multiple channels
    conn = Connection(Configuration())

    # subscribe to any channel you are interested into, with the callback function
    channel = SpotBookTickerChannel(conn, print_message)
    channel.subscribe(symbols)

    # start the client
    await conn.run()


def websockets(lst, *args):
    dict_symbols = {}
    for a, b in lst:
        if dict_symbols.get(a['exchange'], False):
            dict_symbols[a['exchange']] = dict_symbols[a['exchange']] | {a['node']['symbol']}
        else:
            dict_symbols[a['exchange']] = {a['node']['symbol']}
        if dict_symbols.get(b['exchange'], False):
            dict_symbols[b['exchange']] = dict_symbols[b['exchange']] | {b['node']['symbol']}
        else:
            dict_symbols[b['exchange']] = {b['node']['symbol']}


    gate_symbols = [args[0][x] for x in dict_symbols['Gate.io']]

    run_websocket_binance(list(dict_symbols['Binance']))
    threading.Thread(target=ws_bybit, args=(list(dict_symbols['Bybit']),)).start()
    threading.Thread(target=ws_gateio, args=(gate_symbols, )).start()
