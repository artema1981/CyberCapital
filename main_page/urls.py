from django.urls import path
from .views import MainPage, Balances, Statistics, api_form_view
urlpatterns = [
    path('balances/', Balances.as_view(), name='balances'),
    path('statistics/', Statistics.as_view(), name='statistics'),
    path('addapi/', api_form_view, name='addapi'),
    path('', MainPage.as_view(), name='home'),
]
