from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Exchanges
from .forms import AddApiKeyForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from .arbi_alg import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Create your views here.

class MainPage(DataMixin, ListView):
    model = Exchanges
    template_name = 'index.html'
    context_object_name = 'exchanges'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='exchanges')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Exchanges.objects.filter(is_visible=True)


class AddApi(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddApiKeyForm
    template_name = 'addapi.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='addapi')
        return dict(list(context.items()) + list(c_def.items()))

    # def get_queryset(self):
    #     return AddApiKeyForm


# def main_page(request):
#     if request.method == "POST":
#         api_form = AddApiKeyForm(request.POST)
#         if api_form.is_valid():
#             api_form.save()
#
#
#     user = User.objects.filter(is_active=True)
#     exchanges = Exchanges.objects.filter(is_visible=True)
#     api_form = AddApiKeyForm
#     return render(request, 'index.html', context={
#         'title': 'exchanges',
#         'user': user,
#         'exchanges': exchanges,
#         'api_form': api_form,
#     })

def balances(request):
    return render(request, 'balances.html', context={
        'title': 'balances',

    })


def statistics(request):
    return render(request, 'statistics.html', context={
        'title': 'statistics',

    })
