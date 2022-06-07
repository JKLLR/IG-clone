from django.test import TestCase
from .models import Post, UserProfile, Comment
from django.contrib.auth.models import User

# Create your tests here.
class TestUserProfile(TestCase):
    def setUp(self):
        self.user = User(first_name="jeff", last_name="huria",
                         username="jeffhuria", email="jeffhuria@gmail.com",)
        self.user.save()
        self.profile = UserProfile(id=1, user=self.user, bio="my biography",)
        self.profile.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, UserProfile))


class TestPost(TestCase):
    def setUp(self):
        self.user = User(first_name="jeff", last_name="huria",
                         username="jeffhuria", email="jeffhuria21@gmail.com",)
        self.user.save()
        self.profile = UserProfile(user=self.user, bio="my bio",)
        self.profile.save()
        self.test_post = Post(name="Post", caption="test caption", 
                              profile = self.user, user_profile=self.profile)
        self.test_post.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.test_post, Post))