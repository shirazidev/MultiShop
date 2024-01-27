from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError('Users must have a phone address')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given phone, date of
        birth, and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    fullname = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=12, verbose_name='شماره تلفن', unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Check if the user is an admin
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Check if the user is an admin
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # All admins are staff
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expires = models.DateTimeField()

    def __str__(self):
        return str(self.code)

    def is_expired(self):
        return timezone.now() > self.expires

    def save(self, *args, **kwargs):
        # Set the expiration time to 5 minutes from now
        if not self.expires:
            self.expires = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)
