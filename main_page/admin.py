from django.contrib import admin
from .models import Exchanges, AddApiKey, DEMO_Trades

# Register your models here.
admin.site.register(Exchanges)
admin.site.register(AddApiKey)
admin.site.register(DEMO_Trades)