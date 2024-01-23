from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import LoginForm

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
