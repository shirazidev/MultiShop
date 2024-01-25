from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm, CheckOtpForm
from .models import Otp, User
from random import randint
from django.urls import reverse_lazy
import ghasedakpack
import logging

SMS = ghasedakpack.Ghasedak("5d6cefad1e7e9dbddb66e90f224cde86391600b9d1f7254baef7b98c52af4770")


class LoginView(TemplateView):
    http_method_names = ['get', 'post']

    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('phone', 'نام کاربری یا رمز عبور اشتباه است')

        return render(request, "account/login.html", {'form': form})


class RegisterView(TemplateView):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            try:
                SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'djangoetebar', 'param1': randcode})
                print("done")
            except Exception as e:
                print(f"Error sending SMS: {e}")
                # Handle the error, perhaps by displaying a user-friendly message to the user.

            Otp.objects.create(phone=cd["phone"], code=randcode)
            return redirect(reverse_lazy('Account:checkotp') + f'?phone={cd["phone"]}')

        else:
            form.add_error('phone', 'شماره تلفن تکراری است')

        return render(request, "account/register.html", {'form': form})


class CheckOtpView(TemplateView):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/checkotp.html", {'form': form})

    def post(self, request):
        form = CheckOtpForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            phone = cd.get('phone')

            if Otp.objects.filter(code=cd['code'], phone=phone).exists():
                user = User.objects.create_user(phone=phone)
                login(request, user)
                logging.info(f"User with phone {phone} successfully registered.")
                return redirect('Home:home')
            else:
                form.add_error('code', 'کد تایید اشتباه است یا شماره تلفن تکراری است')

        return render(request, "account/checkotp.html", {'form': form})
