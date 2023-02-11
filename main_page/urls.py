from django.urls import path
from .views import MainPage, Balances, Statistics, api_form_view, Exchanges_view
urlpatterns = [
    path('balances/', Balances.as_view(), name='balances'),
    path('statistics/', Statistics.as_view(), name='statistics'),
    path('addapi/', api_form_view, name='addapi'),
    path('exchanges/', Exchanges_view.as_view(), name='exchanges'),
    path('', MainPage.as_view(), name='home'),
]
