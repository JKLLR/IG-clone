from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length = 30)
    bio = models.CharField(max_length=300)
    profile_photo = models.ImageField( default='profile/default.png')

    def __str__(self):
        return self.name



