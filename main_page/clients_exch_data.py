from binance.spot import Spot as Client


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

    def test(self):
        return 'test_ok'
    def get_balance_spot(self):
        balance = self.client.account_snapshot('SPOT')['snapshotVos'][0]['data']['balances']
        balance = list(filter(lambda x: float(x['free']) > 0, balance))

        return balance

    def get_totalAssetOfBtc(self):
        totalAssetOfBtc = self.client.account_snapshot('SPOT')['snapshotVos'][0]['data']['totalAssetOfBtc']
        return totalAssetOfBtc

    def save(self):
        pass