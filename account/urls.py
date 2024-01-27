from django.urls import path
from .views import LogoutView, OtpLoginView, CheckOtpView

app_name = 'account'
urlpatterns = [
    path('login/', OtpLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/checkotp/', CheckOtpView.as_view(), name='otp'),
]
