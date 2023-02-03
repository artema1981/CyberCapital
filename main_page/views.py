from django.shortcuts import render
from .models import Exchanges
from .forms import AddApiKeyForm
from django.contrib.auth.models import User
from .arbi_alg import client


# Create your views here.
def main_page(request):
    if request.method == "POST":
        api_form = AddApiKeyForm(request.POST)
        if api_form.is_valid():
            api_form.save()


    user = User.objects.filter(is_active=True)
    exchanges = Exchanges.objects.filter(is_visible=True)
    api_form = AddApiKeyForm
    # sym = client.exchange_info('GMTUSDT')['symbols'][0]['symbol']
    return render(request, 'index.html', context={
        'user': user,
        'exchanges': exchanges,
        'api_form': api_form,
        # 'sym': sym,
    })
