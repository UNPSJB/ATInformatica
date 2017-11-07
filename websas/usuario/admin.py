from django.contrib import admin
from .models import Usuario

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('persona',)}),
    )

# Register your models here.
admin.site.register(Usuario,MyUserAdmin)


