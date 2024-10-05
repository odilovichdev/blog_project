from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = 'user', 'date_of_birth', 'image'
    list_filter = ['date_of_birth']
