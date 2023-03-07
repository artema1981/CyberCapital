from .clients_exch_data import BinanceApi, GateioApi, BybitApi
import pandas as pd

menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Exchanges', 'url_name': 'exchanges'},
        {'title': 'Balances', 'url_name': 'balances'},
        {'title': 'Bunches', 'url_name': 'bunches'},
        {'title': 'Statistics', 'url_name': 'statistics'},
        {'title': 'Profile', 'url_name': 'profile'}]

exchanges_class_dict = {
    'Binance': BinanceApi,
    'Gate.io': GateioApi,
    'Bybit': BybitApi,
}

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

    def get_exchange(self, key):
        return exchanges_class_dict.get(key)



def gateio_symbol_translate(all_symbols):
    symbol_dict = {}
    for i in [x for x in all_symbols['Gate.io']]:
        newsymbol = i['baseAsset'] + '_' + i['quoteAsset']
        symbol_dict[i['symbol']] = newsymbol

    return symbol_dict

