from django.contrib import admin
from .models import Usuario
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Usuario,UserAdmin)