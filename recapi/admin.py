from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "gender", "date")
    

admin.site.register(UserProfile, UserProfileAdmin)
