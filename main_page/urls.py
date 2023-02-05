from django.urls import path
from .views import main_page, balances, statistics
urlpatterns = [
    path('balances/', balances, name='balances'),
    path('statistics/', statistics, name='statistics'),
    path('', main_page, name='home'),
]
