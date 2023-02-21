from binance.spot import Spot as Client
import time

class ClientsData:
    connected_users = {}

    def __init__(self, user, api_key, secret_key):
        self.user = user
        self.api_key = api_key
        self.secret_key = secret_key


class BinanceApi(ClientsData):

    def __init__(self, user_pk, api_key, secret_key):
        super().__init__(user_pk, api_key, secret_key)
        self.client = Client(api_key, secret_key, base_url='https://api.binance.com')
        BinanceApi.connected_users[user_pk] = self


    def get_balance_spot(self):
        balance = self.client.account_snapshot('SPOT')['snapshotVos'][0]['data']['balances']
        balance = list(filter(lambda x: float(x['free']) > 0, balance))

        return balance

    def get_totalAssetOfBtc(self):
        totalAssetOfBtc = self.client.account_snapshot('SPOT')['snapshotVos'][0]['data']['totalAssetOfBtc']
        return totalAssetOfBtc

    def test_ping(self):
        start_time = time.time()
        ping_response = self.client.ping()
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000

        ping_res=f'{ping_time:.2f} ms'

        start_time1 = time.time()
        server_time = self.client.time()
        end_time1 = time.time()
        request_time1 = (end_time1 - start_time1) * 1000

        request_server_res = f'Request time: {request_time1:.2f}ms'


        start_time2 = time.time()
        ticker = self.client.ticker_price(symbol='BTCUSDT')
        end_time2 = time.time()
        request_time2 = (end_time2 - start_time2) * 1000

        request_ticker_res = f'Request time: {request_time2:.2f}ms'


        return ping_res