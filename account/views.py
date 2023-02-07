from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from main_page.utils import DataMixin
from .forms import RegistrationForm, LoginForm
from django.views.generic import ListView, DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import User, UserCreationForm


# Create your views here.
# def login_view(request):
#     form = LoginForm(request.POST or None)
#     next_get = request.GET.get('next')
#
#     if form.is_valid():
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#         login(request, user)
#
#         next_post = request.POST.get('next')
#
#         return redirect(next_get or next_post or '/')
#
#     return render(request, 'login.html', context={'form': form,
#                                                   'title': 'login'})

def logout_view(request):
    logout(request)
    return redirect('/')



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