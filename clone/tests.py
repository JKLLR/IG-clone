from django.test import TestCase
from .models import Profile, Post
from django.contrib.auth.models import User

# Create your tests here.

class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='jeff')
        self.user.save()

        self.profile_test = Profile(id=1, name='image', profile_pic='default.jpg', bio='bio test',
                                    user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile_test, Profile))

    def test_save_profile(self):
        self.profile_test.save_profile()
        after = Profile.objects.all()
        self.assertTrue(len(after) > 0)