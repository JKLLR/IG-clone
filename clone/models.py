from django.db import models
from django.contrib.auth.models import User

# Create your models here.
profile_photo = models.ImageField( default='profile/default.png')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField( default='profile/default.png')
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return self.bio

    @classmethod
    def search_by_user(cls,search_term):
        instauser = cls.objects.filter(user__icontains=search_term)
        return instauser


