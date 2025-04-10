from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'favorite_genres', 'role')
    search_fields = ('user__username', 'favorite_genres')
    list_filter = ('role',)
