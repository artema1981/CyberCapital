from django.urls import path
from .views import *

urlpatterns = [
    path('balances/', Balances.as_view(), name='balances'),
    path('statistics/', Statistics.as_view(), name='statistics'),
    path('exchanges/', Exchanges_view.as_view(), name='exchanges'),
    path('bunches/', Bunches_view.as_view(), name='bunches'),
    path('', MainPage.as_view(), name='home'),
    path('api/', ApiCreateView.as_view(), name='api_add'),
    path('api/<int:pk>', ApiUpdateView.as_view(), name='api_update'),
    path('api/<int:pk>/delete', ApiDeleteView.as_view(), name='api_delete'),
    path('exchanges/connect', Connect.as_view(), name='connect'),

]
