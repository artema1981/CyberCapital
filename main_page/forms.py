from django import forms
from .models import AddApiKey, Exchanges
from django.contrib.auth.models import User
class AddApiKeyForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={
        'id': "select-f1e4",
        'name': "select",
        'class': "u-border-1 u-border-grey-30 u-input u-input-rectangle u-white",
        'required': "required"
    }))

    exchange = forms.ModelChoiceField(queryset=Exchanges.objects.all(), widget=forms.Select(attrs={
        'id': "select-f1e4",
        'name': "select",
        'class': "u-border-1 u-border-grey-30 u-input u-input-rectangle u-white",
        'required': "required"
    }))
    api_key = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        'placeholder': "Enter your api key",
        'id': "name-3b9a",
        'name': "api key",
        'class': "u-border-1 u-border-grey-30 u-input u-input-rectangle u-white",
        'required': ""
    }))
    secret_api_key = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        'placeholder': "Enter your api key",
        'id': "name-3b9a",
        'name': "api key",
        'class': "u-border-1 u-border-grey-30 u-input u-input-rectangle u-white",
        'required': ""
    }))
    class Meta:
        model = AddApiKey
        fields = ('user', 'exchange', 'api_key', 'secret_api_key')