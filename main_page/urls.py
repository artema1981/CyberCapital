from django.urls import path
from .views import MainPage, balances, statistics, api_form_view
urlpatterns = [
    path('balances/', balances, name='balances'),
    path('statistics/', statistics, name='statistics'),
    path('addapi/', api_form_view, name='addapi'),
    path('', MainPage.as_view(), name='home'),
]
