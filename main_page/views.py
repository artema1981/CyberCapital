import pandas as pd
from asgiref.sync import sync_to_async
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from .clients_exch_data import *
from .models import Exchanges, AddApiKey
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, FormView, UpdateView, DeleteView
from .utils import DataMixin, gateio_symbol_translate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from .redis_db import *
from .arbi_alg import websockets

# Create your views here.
def read(filename):
    with open(filename, 'r', encoding= 'utf-8') as file:
        return json.load(file)

class MainPage(DataMixin, ListView):
    model = Exchanges
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Cyber Capital')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return 'Cyber Capital'


class Exchanges_view(LoginRequiredMixin, DataMixin, ListView):
    model = Exchanges
    template_name = 'exchanges.html'
    context_object_name = 'exchanges'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # update dict DatMixin
        c_def = self.get_user_context(title='exchanges')
        # render list exchange/key for auth user
        users_key = AddApiKey.objects.filter(user_profile_id=self.request.user.pk)
        context['users_key'] = users_key
        exchange_list = []
        for exchange in context['exchanges']:
            exchange_list.append({'exchange': exchange,
                                  'exchange_obj': context['exchanges'],
                                  'api': None,
                                  'ping': get_redis(f'{self.request.user.pk}_{exchange.name}')})
            for api in context['users_key']:
                if api.exchange == exchange:
                    exchange_list[-1]['api'] = api.api_key
                    exchange_list[-1]['api_pk'] = api.pk
        context['exchange_list'] = exchange_list

        return dict(list(context.items()) + list(c_def.items()))


class ApiCreateView(CreateView):
    model = AddApiKey
    fields = ['api_key', 'secret_api_key']
    success_url = reverse_lazy('exchanges')

    def form_valid(self, form):
        order = form.save(commit=False)

        # put in the form exchange id
        get_exchange = Exchanges.objects.get(name=self.request.GET['exchange_id'])
        order.exchange = get_exchange

        # put in the form users id
        order.user_profile = self.request.user

        self.object = order.save()
        return super().form_valid(form)


class ApiUpdateView(UpdateView):
    model = AddApiKey
    fields = ['api_key', 'secret_api_key']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('exchanges')


class ApiDeleteView(DeleteView):
    model = AddApiKey
    success_url = reverse_lazy('exchanges')


class Connect(DataMixin, View):

    def get(self, request):
        ping_life = 30
        exchange = request.GET.get('exchange')
        user_pk = self.request.user.pk
        api = AddApiKey.objects.get(pk=int(request.GET.get('api_pk')))
        Exchange_Api = self.get_exchange(exchange)
        client_instance = Exchange_Api(user_pk, api.api_key, api.secret_api_key)
        set_redis(f'{user_pk}_{exchange}', client_instance.test_ping(), ex=ping_life)
        return redirect('exchanges')






class Balances(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'balances.html'
    context_object_name = 'balances'

    @staticmethod
    def render_bunch(balances_lst, exchange_lst, all_symbols):
        all_balances = {}
        for i in range(len(exchange_lst)):
            all_balances[exchange_lst[i]] = balances_lst[i]
        n = len(exchange_lst)
        x = 0
        bunches_list = []
        def close(coin, exchange):
            for i in range(x, n):
                for coin2 in all_balances[exchange_lst[i]]:
                    f1_coin = list(
                        filter(lambda x: x['baseAsset'] == coin and x['quoteAsset'] == coin2, all_symbols[exchange]))
                    f2_coin = list(
                        filter(lambda x: x['baseAsset'] == coin2 and x['quoteAsset'] == coin, all_symbols[exchange]))
                    node1 = f1_coin if f1_coin else f2_coin

                    f1_coin2 = list(filter(lambda x: x['baseAsset'] == coin and x['quoteAsset'] == coin2,
                                           all_symbols[exchange_lst[i]]))
                    f2_coin2 = list(filter(lambda x: x['baseAsset'] == coin2 and x['quoteAsset'] == coin,
                                           all_symbols[exchange_lst[i]]))
                    node2 = f1_coin2 if list(f1_coin2) else f2_coin2
                    if node1 and node2:
                        res = [{'exchange': exchange, 'coin': coin, 'free': all_balances[exchange][coin],
                                'node': node1[0]},
                               {'exchange': exchange_lst[i], 'coin': coin2,
                                'free': all_balances[exchange_lst[i]][coin2], 'node': node2[0]}]
                        bunches_list.append(res)  # exchange, (coin, coin2), exchange_lst[i])

        for i in range(n - 1):
            x += 1
            for coin in all_balances[exchange_lst[i]]:
                close(coin, exchange_lst[i])


        websockets(bunches_list, gateio_symbol_translate(all_symbols))
        return bunches_list
    def get_balances(self):
        """
        Chart balances all accounts
        """
        connect_data = AddApiKey.objects.filter(user_profile_id=self.request.user.pk)
        if not connect_data:
            return '<h3>You have not any one connected  exchange</h3>'
        demo = True
        all_symbols = {}  # {'Binance': ['ETHBTC', 'LTCBTC'..., 'Bybit': [['ETHBTC', 'LTCBTC'...,
        exchange_lst = []
        balances_lst = []
        set_coins = set()

        if demo:

            all_symbols = read('demofiles/all_symbols.json')
            exchange_lst = read('demofiles/exchange_lst.json')
            balances_lst = read('demofiles/balances_lst.json')
            lst_coin = [x.keys() for x in balances_lst]
            set_coins = set()
            for i in lst_coin:
                set_coins = set_coins | set(i)
        else:

            for i in connect_data:
                exchange_lst.append(i.exchange.name)
                Exchange_Api = self.get_exchange(i.exchange.name)
                client_instance = Exchange_Api(i.user_profile.pk, i.api_key, i.secret_api_key)
                balance = client_instance.get_balance_spot()
                balances_lst.append(balance)
                set_coins = set_coins | set(balance.keys())
                all_symbols[i.exchange.name] = client_instance.get_all_symbols_list()




        coins_list = list(set_coins)
        bunches_list = Balances.render_bunch(balances_lst, exchange_lst, all_symbols)
        df_list = []
        for i in range(len(exchange_lst)):
            bal_dict_s = pd.Series(data=balances_lst[i], index=coins_list)
            df_list.append(pd.DataFrame({'coin': coins_list,
                                         exchange_lst[i]: bal_dict_s.values}))

        res = df_list[0]
        if len(df_list) > 1:
            for i in range(1, len(df_list)):
                res = res.join(df_list[i].set_index('coin'), on='coin')

        return {'balance_chart': res, 'bunches_list': bunches_list}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='balances')
        if isinstance(self.get_balances(), str):
            context['balance_chart'] = self.get_balances()['balance_chart']
        else:
            context['balance_chart'] = self.get_balances()['balance_chart'].to_html()
            context['bunches_list'] = self.get_balances()['bunches_list']
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return 'balances'


class Statistics(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'statistics.html'
    context_object_name = 'statistics'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='statistics')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return 'statistics'


class Bunches_view(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'bunches.html'
    context_object_name = 'bunches'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='bunches')
        print()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return 'bunches'
