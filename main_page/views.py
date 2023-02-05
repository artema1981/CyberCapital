from django.shortcuts import render
from .models import Exchanges
from .forms import AddApiKeyForm
from django.contrib.auth.models import User
from .arbi_alg import *


# Create your views here.
def main_page(request):
    if request.method == "POST":
        api_form = AddApiKeyForm(request.POST)
        if api_form.is_valid():
            api_form.save()


    user = User.objects.filter(is_active=True)
    exchanges = Exchanges.objects.filter(is_visible=True)
    api_form = AddApiKeyForm
    return render(request, 'index.html', context={
        'title': 'exchanges',
        'user': user,
        'exchanges': exchanges,
        'api_form': api_form,
    })

def balances(request):
    return render(request, 'balances.html', context={
        'title': 'balances',

    })

def statistics(request):
    return render(request, 'statistics.html', context={
        'title': 'statistics',

    })