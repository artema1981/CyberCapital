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

def api_form_view(request):
    if request.method == "POST":
        api_form = AddApiKeyForm(request.POST)
        if api_form.is_valid():
            order = api_form.save(commit=False)
            order.user_profile = request.user
            order.save()


    api_form = AddApiKeyForm
    return render(request, 'addapi.html', context={
        'api_form': api_form,
    })
# class AddApi(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = AddApiKeyForm
#     template_name = 'addapi.html'
#     login_url = reverse_lazy('login')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='addapi')
#         return dict(list(context.items()) + list(c_def.items()))

    # def get_queryset(self):
    #     return AddApiKeyForm


def balances(request):
    return render(request, 'balances.html', context={
        'title': 'balances',

    })

def statistics(request):
    return render(request, 'statistics.html', context={
        'title': 'statistics',

    })
