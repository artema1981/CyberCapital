from django.shortcuts import render
from .models import Exchanges

# Create your views here.
def main_page(request):
    exchanges = Exchanges.objects.filter(is_visible=True)
    return render(request, 'index.html', context={
        'exchanges': exchanges
    })
