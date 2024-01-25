from django.urls import path
from . import views

app_name = "Account"
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('register/checkotp', views.CheckOtpView.as_view(), name='checkotp'),
]