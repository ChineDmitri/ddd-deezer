from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorite_genres = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('artist', 'Artist'), ('listener', 'Listener'), ('admin', 'admin')], default='listener')

    def __str__(self):
        return f"{self.user.username}'s Profile"
