from django.db import models
import uuid
import os
from django.contrib.auth.models import User

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


class AddApiKey(models.Model):

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchanges, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=250, unique=True)
    secret_api_key = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'user: {self.user} exchange: {self.exchange} api_key:{self.api_key} secret_api_key{self.secret_api_key}'
