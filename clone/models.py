from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField

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
    def search_user(cls,username):
        return User.objects.filter(username = username)


class Post(models.Model):
    image = ImageField('image/')
    name = models.CharField(max_length=144, blank=True, default="Post")
    caption = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
   
    
    def __str__(self):
        return f"{self.name} - {self.caption}"

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    def update_caption(self, new_cap):
        self.caption = new_cap
        self.save()


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment