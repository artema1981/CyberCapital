from .models import AddApiKey

menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Exchanges', 'url_name': 'exchanges'},
        # {'title': 'Api', 'url_name': 'addapi'},
        {'title': 'Balances', 'url_name': 'balances'},
        {'title': 'Statistics', 'url_name': 'statistics'},
        {'title': 'Profile', 'url_name': 'profile'}]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

