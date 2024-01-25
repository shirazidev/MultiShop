# forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators
from .models import User

def start_with_0(value):
    if not value or value[0] != '0':
        raise forms.ValidationError("شماره تلفن باید با صفر شروع شود")

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تایید گذرواژه", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["phone",]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "password", "is_active", "is_admin"]

class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
        validators=[start_with_0, validators.MaxLengthValidator(11), validators.MinLengthValidator(10)]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )

class RegisterForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
        validators=[start_with_0, validators.MaxLengthValidator(11), validators.MinLengthValidator(10)]
    )

class CheckOtpForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد ارسالی'}),
        validators=[validators.MaxLengthValidator(4), validators.MinLengthValidator(4)]
    )
    phone = forms.CharField(widget=forms.HiddenInput())
