from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm
import ghasedakpack
from random import randint

SMS = ghasedakpack.Ghasedak("5d6cefad1e7e9dbddb66e90f224cde86391600b9d1f7254baef7b98c52af4770")


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('admin:index')
            else:
                return redirect('Home:home')
        else:
            form = LoginForm()
            return render(request, "account/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('account:login')
            else:
                form.add_error('phone', 'invalid data')

        else:
            form.add_error('phone', 'invalid data')

        return render(request, "account/login.html", {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('admin:index')
            else:
                return redirect('Home:home')
        else:
            form = RegisterForm()
            return render(request, "account/register.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000,9999)
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'djangoetebar', 'param1': randcode})
            print(randcode)
            print("done")

        else:
            form.add_error('phone', 'invalid data')

        return render(request, "account/login.html", {'form': form})
# ta ghesmate 2