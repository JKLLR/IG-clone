from django.urls import path
from . import views


urlpatterns=[
    path('',views.login_page, name='login'),
    path('index/',views.index, name="index"),
    path('register/', views.register, name='register'),
    path('post/',views.post, name="post"),
]