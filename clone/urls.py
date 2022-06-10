from django.urls import path
from . import views


urlpatterns=[
    path('',views.post, name='post'),
    path('login/',views.login_page, name="login"),
    path('register/', views.register, name='register'),
    path('logout/',views.logout, name="logout"),
    path('search/', views.search_results, name='search_results'),
    path('image/(<image_id>\d+)',views.image,name ='image'),
    path('comments/<int:pk>' , views.new_comment, name='comment'),
    path('comments/(<pk>\d+)' , views.new_comment, name='comment'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('profile/', views.profile, name='profile'),
    path('like/(<image_id>\d+)',views.like, name = 'postlike'),


  
]