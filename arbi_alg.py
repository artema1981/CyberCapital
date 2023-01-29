from main_page.models import Exchanges

def get_exchages():
    print(Exchanges.objects.all())





# binance_api_balance = {'USDT': 10000, 'BTC': 0.5, 'XRP': 30000 }
# bybit_api_balance = {'USDT': 10000, 'BTC': 0.5, 'ETH': 10 }
# poloniex_api_balance = {'USDT': 10000, 'BTC': 0.5, 'ADA': 40000 }
#
#
#
#
#
# class Exchenges:
#
#     def __init__(self, name, spot_free, wsocket='', api=''):
#         self.name = name
#         self.spot_free = spot_free
#         self.wsocket = wsocket
#         self.api = api
#         self.api_key = ''
#         self.api_secret_key = ''
#         self.balance = {}
#
#     def upload_blance(self):
#         self.balance = {}#api connect
#
#     def get_symbol_balance(self, symbol):
#         pass
#         #returne {baseAsset: vol quoteAsset: vol}
#
#
# class Bunch:
#
#     def __init__(self, exchenge_1, exchenge_2, symbol):
#         self.exchenge_1 = exchenge_1
#         self.exchenge_2 = exchenge_2
#         self.symbol = symbol
#         self.exchenge_1_balance = 0
#         self.exchenge_2_balance = 0
#
#     def set_balans(self):
#         self.exchenge_1_balance = self.exchenge_1.get_balance(self.symbol)
#         self.exchenge_2_balance = self.exchenge_1.get_balance(self.symbol)
#
#     def __str__(self):
#         return
#
#
# # class Arbitr_screener:
# #     PROFIT_PERCENT = 0.5
# #
# #     def __init__(self, bunch):
# #         self.bunch = bunch
#
# PROFIT_PERCENT = 0.5
# Binance = Exchenges('Binance', 0.075)
# Bybit = Exchenges('Bybit', 0.1)
# Poloniex = Exchenges('Poloniex', 0.15)
#
# buch1 = Bunch(Bybit, Binance, 'BTSUSDT')
# buch1.set_balans()
#
#
#
# def check_buy_sell(bunch):
#
#     investment_amount1 = initial_investment
#     current_price1 = fetch_current_ticker_price(scrip1)['ask']
#     final_price = 0
#     scrip_prices = {}
#     if current_price1 is not None: #and not check_if_float_zero(current_price1):
#         buy_quantity1 = round(investment_amount1 / current_price1, 8)
#
#
#         ## SCRIP2
#         investment_amount2 = buy_quantity1
#         current_price2 = fetch_current_ticker_price(scrip2)['bid']
#         if current_price2 is not None:# and not check_if_float_zero(current_price2):
#             sell_quantity2 = buy_quantity1
#             sell_price2 = round(sell_quantity2 * current_price2, 8)
#
#
#             ## SCRIP1
#             investment_amount3 = sell_price2
#             current_price3 = fetch_current_ticker_price(scrip3)['bid']
#             if current_price3 is not None:# and not check_if_float_zero(current_price3):
#                 sell_quantity3 = sell_price2
#                 final_price = round(sell_quantity3 * current_price3, 3)
#                 scrip_prices = {scrip1: current_price1, scrip2: current_price2, scrip3: current_price3}
#     return final_price, scrip_prices
#











