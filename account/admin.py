from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Otp


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('fullname', 'phone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ("اطلاعات کاربری", {'fields': ('phone', 'password',)}),
        ('اطلاعات شخصی', {'fields': ("fullname",)}),
        ('دسترسی ها', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'fullname', 'password1', 'password2'),
        }),
    )
    search_fields = ("fullname",)
    ordering = ('fullname',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Otp)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
