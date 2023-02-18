from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from .models import Exchanges, AddApiKey
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, FormView, UpdateView, DeleteView
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


# Create your views here.

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
        c_def = self.get_user_context(title='exchanges')
        users_key = AddApiKey.objects.filter(user_profile_id=self.request.user.pk)
        context['users_key'] = users_key
        exchange_list = []
        for exchange in context['exchanges']:
            exchange_list.append({'exchange': exchange,
                                  'exchange_obj': context['exchanges'],
                                  'api': None})
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
        get_exchange = Exchanges.objects.get(name=self.request.GET['name1'])
        order.user_profile = self.request.user
        order.exchange = get_exchange
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


class Balances(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'balances.html'
    context_object_name = 'balances'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='balances')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return 'balance.objects.filter(is_visible=True)'


class Statistics(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'statistics.html'
    context_object_name = 'statistics'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='statistics')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return 'statistics'
