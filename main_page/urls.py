from django.urls import path
from .views import MainPage, Balances, Statistics,  Exchanges_view, ApiCreateView, ApiUpdateView, ApiDeleteView
urlpatterns = [
    path('balances/', Balances.as_view(), name='balances'),
    path('statistics/', Statistics.as_view(), name='statistics'),
    path('exchanges/', Exchanges_view.as_view(), name='exchanges'),
    path('', MainPage.as_view(), name='home'),
    # path('addapi/', Api_form_view.as_view, name='addapi'),
    path('api', ApiCreateView.as_view(), name='api-add'),
    path('api/<int:pk>/', ApiUpdateView.as_view(), name='api-update'),
    path('api_form/<int:pk>/delete/', ApiDeleteView.as_view(), name='api-delete'),

]
