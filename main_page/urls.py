from django.urls import path
from .views import main_page, balances
urlpatterns = [
    path('', main_page),
]
