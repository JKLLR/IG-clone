# Generated by Django 4.0.5 on 2022-06-08 23:50

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clone', '0002_comment_post_userprofile_delete_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='profile_pic'),
        ),
    ]
