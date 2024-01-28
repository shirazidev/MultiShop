from django.db import transaction
from uuid import uuid4

import ghasedakpack
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views import View
from random import randint
from .forms import LoginForm, RegisterForm
from .forms import OtpForm
from .models import Otp
from .models import User

SMS = ghasedakpack.Ghasedak("5d6cefad1e7e9dbddb66e90f224cde86391600b9d1f7254baef7b98c52af4770")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class OtpLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('admin:index')
            else:
                return redirect('Home:home')
        else:
            form = RegisterForm()
            return render(request, "account/otp-login.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)

            try:
                with transaction.atomic():
                    # Send verification code via SMS
                    SMS.verification(
                        {'receptor': cd['phone'], 'type': '1', 'template': 'djangoetebar', 'param1': randcode})
                    print(randcode)
                    token = str(uuid4())
                    # Create Otp object
                    Otp.objects.create(phone=cd['phone'], code=randcode, token=token)

                    # Redirect to OTP verification page
                    return redirect(reverse('account:otp') + f'?token={token}')

            except Exception as e:
                # Handle SMS sending error or any other exception
                print(f"Error: {e}")
                form.add_error('phone', 'Error sending verification code. Please try again.')

        else:
            form.add_error('phone', 'Invalid data')

        return render(request, "account/otp-login.html", {'form': form})


class CheckOtpView(View):
    def get(self, request):
        token = request.GET.get('token')

        # Check if the provided token exists in the database
        otp_instance = Otp.objects.filter(token=token).first()

        if otp_instance:
            # Check if the OTP is expired
            if otp_instance.expires > timezone.now():
                # Calculate remaining time in seconds
                remaining_time_seconds = (otp_instance.expires - timezone.now()).total_seconds()

                # Convert remaining time to a positive integer
                remaining_time_seconds = max(0, round(remaining_time_seconds))

                return render(request, "account/check-otp.html",
                              {'form': OtpForm(), 'remaining_time_seconds': remaining_time_seconds})
            else:
                return redirect('account:login')  # Redirect to register page if the token is expired
        else:
            # Token not found in the database
            return redirect('account:login')  # Redirect to register page if the token does not exist

    def post(self, request):
        token = request.GET.get('token')
        form = OtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Check if the provided OTP matches the stored OTP for the given phone
            otp_instance = Otp.objects.filter(code=cd['code'], token=token).first()

            if otp_instance:
                # Check if the OTP is expired
                if otp_instance.is_expired():
                    form.add_error('code', 'Expired OTP')
                else:
                    # OTP is valid, create user and log in
                    user, is_created = User.objects.get_or_create(phone=otp_instance.phone)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # Optionally, you may want to delete the used OTP instance here
                    otp_instance.delete()
                    return redirect('Home:home')
            else:
                # Invalid OTP
                form.add_error('code', 'Invalid OTP')

        else:
            # Form is not valid
            form.add_error('code', 'Invalid data')

        return render(request, "account/check-otp.html", {'form': form})
