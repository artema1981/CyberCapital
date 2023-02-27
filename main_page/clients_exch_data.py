from binance.spot import Spot as Client
from pybit import spot
import time
import hashlib
import hmac
import requests
import json


class ClientsData:

    def __init__(self, user, api_key, secret_key):
        self.user = user
        self.api_key = api_key
        self.secret_key = secret_key

    def get_all_symbols_list(self):
        return 'pass'

class BinanceApi(ClientsData):

    def __init__(self, user_pk, api_key, secret_key):
        super().__init__(user_pk, api_key, secret_key)
        self.client = Client(api_key, secret_key, base_url='https://api.binance.com')

    def get_balance_spot(self):
        balance = self.client.account_snapshot('SPOT')['snapshotVos'][0]['data']['balances']
        balance = list(filter(lambda x: float(x['free']) > 0, balance))
        res_dict = {}
        for i in balance:
            res_dict[i['asset']] = i['free']
        return res_dict

    def get_totalAssetOfBtc(self):
        totalAssetOfBtc = self.client.account_snapshot('SPOT')['snapshotVos'][0]['data']['totalAssetOfBtc']
        return totalAssetOfBtc

    def get_all_symbols_list(self):
        lst_symbols = []
        ex_info = self.client.exchange_info()
        for i in ex_info['symbols']:
            symbol = {'symbol': i['symbol'], 'baseAsset': i['baseAsset'], 'quoteAsset':i['quoteAsset']}
            if i['isSpotTradingAllowed'] and i['status'] == 'TRADING':
                lst_symbols.append(symbol)
        return lst_symbols


    def test_ping(self):
        start_time = time.time()
        ping_response = self.get_balance_spot()  # self.client.ping()
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000
        ping_res = f'{ping_time:.2f} ms'

        start_time1 = time.time()
        server_time = self.client.time()
        end_time1 = time.time()
        request_time1 = (end_time1 - start_time1) * 1000
        request_server_res = f'{request_time1:.2f}ms'

        start_time2 = time.time()
        ticker = self.client.ticker_price(symbol='BTCUSDT')
        end_time2 = time.time()
        request_time2 = (end_time2 - start_time2) * 1000
        request_ticker_res = f'Request time: {request_time2:.2f}ms'

        return request_server_res


class GateioApi(ClientsData):

    def __init__(self, user_pk, api_key, secret_key):
        super().__init__(user_pk, api_key, secret_key)
        self.host = "https://api.gateio.ws"
        self.prefix = "/api/v4"
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def gen_sign(self, method, url, query_string=None, payload_string=None):
        t = time.time()
        m = hashlib.sha512()
        m.update((payload_string or "").encode('utf-8'))
        hashed_payload = m.hexdigest()
        s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
        sign = hmac.new(self.secret_key.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': self.api_key, 'Timestamp': str(t), 'SIGN': sign}

    def get_balance_spot(self):
        url = '/spot/accounts'
        query_param = ''
        sign_headers = self.gen_sign('GET', self.prefix + url, query_param)
        self.headers.update(sign_headers)
        r = requests.request('GET', self.host + self.prefix + url, headers=self.headers)

        res_dict = {}
        for i in r.json():
            res_dict[i['currency']] = i['available']

        return res_dict

    def get_all_symbols_list(self):
        host = "https://api.gateio.ws"
        prefix = "/api/v4"
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = '/spot/currency_pairs'
        query_param = ''
        r = requests.request('GET', host + prefix + url, headers=headers)
        res = [{'symbol': x['base']+x['quote'], 'baseAsset': x['base'], 'quoteAsset': x['quote']} for x in r.json()]
        return res


    def test_ping(self):
        start_time = time.time()
        ping_response = self.get_balance_spot()
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000
        ping_res = f'{ping_time:.2f} ms'

        start_time1 = time.time()
        server_time = self.get_balance_spot()
        end_time1 = time.time()
        request_time1 = (end_time1 - start_time1) * 1000
        request_server_res = f'{request_time1:.2f} ms'

        return request_server_res

class BybitApi(ClientsData):

    def __init__(self, user_pk, api_key, secret_key):
        super().__init__(user_pk, api_key, secret_key)
        self.client = spot.HTTP(api_key=api_key, api_secret=secret_key, endpoint='https://api-testnet.bybit.com')

    def get_balance_spot(self):
        balance = self.client.get_wallet_balance()['result']['balances']
        # balance = list(filter(lambda x: float(x['free']) > 0, balance))
        res_dict = {}
        for i in balance:
            res_dict[i['coin']] = i['free']
        return res_dict

    def get_all_symbols_list(self):
        url = "https://api.bybit.com/spot/v3/public/symbols"
        response = requests.get(url)
        if response.status_code == 200:
            symbols = response.json()["result"]
            ticker_list = [{ 'symbol': symbol["name"], 'baseAsset': symbol['baseCoin'], 'quoteAsset': symbol['quoteCoin']} for symbol in symbols['list']]
            return ticker_list
        else:
            return "Failed to retrieve ticker list."

    def test_ping(self):
        start_time = time.time()
        ping_response = self.get_balance_spot()
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000
        ping_res = f'{ping_time:.2f} ms'

        start_time1 = time.time()
        server_time = self.get_balance_spot()
        end_time1 = time.time()
        request_time1 = (end_time1 - start_time1) * 1000
        request_server_res = f'{request_time1:.2f} ms'

        return request_server_res