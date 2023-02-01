from django.shortcuts import render
from .models import Exchanges
from .forms import AddApiKeyForm
from django.contrib.auth.models import User
# Create your views here.
def main_page(request):
    if request.method == "POST":
        api_form = AddApiKeyForm(request.POST)
        if api_form.is_valid():
            api_form.save()
        if not api_form.is_valid():
            pass


    user = User.objects.filter(is_active=True)
    exchanges = Exchanges.objects.filter(is_visible=True)
    api_form = AddApiKeyForm
    return render(request, 'index.html', context={
        'user': user,
        'exchanges': exchanges,
        'api_form': api_form,
    })
