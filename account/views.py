from django.contrib.auth.views import LoginView, redirect_to_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View

from main_page.utils import DataMixin
from .forms import RegistrationForm, LoginForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import User, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile




class RegisterUser(DataMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    logout(request)
    return redirect('/')


# @login_required
# def profile(request):
#     return render(request, 'profile.html')
class ProfilePage(LoginRequiredMixin, DataMixin, ListView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='profile')
        print(dict(list(context.items()) + list(c_def.items())))
        return dict(list(context.items()) + list(c_def.items()))

    def get_user_context(self, **kwargs):
        return super(ProfilePage, self).get_user_context(**kwargs)