from django.db import models
import uuid
import os
from django.contrib.auth.models import User
from django.urls import reverse

from account.models import Profile

# Create your models here.
class Exchanges(models.Model):
    def get_file_name(self, filname: str):
        ext = filname.strip().split('.')[-1]
        filname = f'{uuid.uuid4()}.{ext}'
        return os.path.join('images/logos', filname)

    name = models.CharField(max_length=50)
    api_connect = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    logo = models.ImageField(upload_to=get_file_name)
    position = models.SmallIntegerField()
    ping = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)

# def get_pofile_user_id():
#     return Profile.pk
class AddApiKey(models.Model):

    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchanges, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=250)
    secret_api_key = models.CharField(max_length=250)

    def __str__(self):
        return f'user: {self.user_profile.pk} exchange: {self.exchange} api_key:{self.api_key} secret_api_key:{self.secret_api_key}'

    def get_absolute_url(self):
        return reverse('api_update', kwargs={'pk': self.pk})

class DEMO_Trades(models.Model):

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bunch = models.JSONField()
    trade = models.JSONField()
    profit = models.DecimalField(max_digits=19, decimal_places=6)




































