# Generated by Django 4.1.3 on 2022-12-04 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_user_alter_post_author_alter_post_likes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
