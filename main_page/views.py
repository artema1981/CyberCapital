from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Exchanges, AddApiKey
from .forms import AddApiKeyForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
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


class Exchanges_view(DataMixin, ListView):
    model = Exchanges
    template_name = 'exchanges.html'
    context_object_name = 'exchanges'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='exchanges')
        c_def2 = self.get_api()
        print(type(dict(list(context.items()))),  type(list(c_def.items())))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Exchanges.objects.filter(is_visible=True)


def api_form_view(request):
    if request.method == "POST":
        api_form = AddApiKeyForm(request.POST)
        if api_form.is_valid():
            order = api_form.save(commit=False)
            order.user_profile = request.user
            order.save()

    api_form = AddApiKeyForm
    context = {
        'menu': menu,
        'api_form': api_form
    }
    return render(request, 'addapi.html', context=context)


# class Api_view(LoginRequiredMixin, DataMixin, ListView):
#     model = AddApiKey
#     template_name = 'exchanges.html'
#     context_object_name = 'api'
#
#     def get_queryset(self):
#         return  AddApiKey.objects.all()#AddApiKey.objects.filter(user_profile=request.user)




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
