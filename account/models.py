# models.py
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, fullname=None, email=None, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone=phone,
            email=email,
            fullname=fullname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, fullname, email=None, password=None):
        user = self.create_user(
            phone=phone,
            email=email,
            fullname=fullname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    fullname = models.CharField(max_length=150, verbose_name="نام کامل")
    phone = models.CharField(max_length=12, unique=True, verbose_name="شماره تلفن")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["fullname", ]

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=255, verbose_name="توکن")
    phone = models.CharField(max_length=11, verbose_name="شماره تلفن")
    code = models.SmallIntegerField(verbose_name="کد تایید")
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)
