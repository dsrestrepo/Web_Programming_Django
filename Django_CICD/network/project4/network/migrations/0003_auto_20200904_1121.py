# Generated by Django 3.1 on 2020-09-04 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_followers_likes_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='user',
            new_name='users',
        ),
    ]
