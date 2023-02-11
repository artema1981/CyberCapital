from .models import AddApiKey

api_dict = [x.__dict__ for x in list(AddApiKey.objects.iterator())]

menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Exchanges', 'url_name': 'exchanges'},
        {'title': 'Api', 'url_name': 'addapi'},
        {'title': 'Balances', 'url_name': 'balances'},
        {'title': 'Statistics', 'url_name': 'statistics'},
        {'title': 'Profile', 'url_name': 'profile'}]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

    def get_api(self, **kwargs):
        context = kwargs
        context['api_dict'] = api_dict
        return context