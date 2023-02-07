

menu = [{'title': 'Exchanges', 'url_name': 'home'},
        {'title': 'Api', 'url_name': 'addapi'},
        {'title': 'Balances', 'url_name': 'balances'},
        {'title': 'Statistics', 'url_name': 'statistics'}]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
