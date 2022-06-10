from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    name=models.CharField(blank=True,max_length=120)
    # profile_pic=models.ImageField(upload_to='pictures/',default='default.png')
    profile_pic= CloudinaryField('image')

    bio=models.TextField(max_length=400,blank=True)
    location=models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()  

    @classmethod
    def update_bio(cls,id,bio):
        update_profile = cls.object.filter(id=id).update(bio=bio) 
        return update_profile 

    @classmethod
    def search_profile(cls,search_term) :
        profiles=cls.objects.filter(user__username__icontains=search_term) 
        return profiles 
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()         

class Post(models.Model):
    image_post= CloudinaryField('image')
    # image_post=models.ImageField(upload_to='posts/')
    name= models.CharField(max_length=250,blank=True)
    caption= models.CharField(max_length=250,blank=True)
    created_at=models.DateField(auto_now_add=True, null=True)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', null=True)
    class Meta:
        '''
        Class method to display images by date published
        '''
        ordering = ['created_at']
    
    def save_post(self):
        '''
        Method to save our post
        '''
        self.save()

    def delete_post(self):
        '''
        Method to delete our post
        '''
        self.delete()    

    def __str__(self):
        return self.name
    @property
    def num_liked(self):
        return self.liked.all().count()

    @classmethod
    def update_caption(cls, self, caption):
        update_cap = cls.objects.filter(id = id).update(caption = caption)
        return update_cap    

# LIKE_CHOICES = (
#     ('Like', 'Like'),
#     ('Unlike', 'Unlike'),
# )
# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null = True)
#     value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10, null = True)

#     def __str__(self):
#         return self.post    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name='comments')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add =True,null=True)
    
    def __str__(self):
        return f'{self.post}'

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'

class Subscribers(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()   

class Like(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='user_like')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_likes')      