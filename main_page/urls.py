from django.urls import path
from .views import MainPage, balances, statistics, AddApi
urlpatterns = [
    path('balances/', balances, name='balances'),
    path('statistics/', statistics, name='statistics'),
    path('addapi/', AddApi.as_view(), name='addapi'),
    path('', MainPage.as_view(), name='home'),
]
