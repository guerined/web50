from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models



class User(AbstractUser):
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, default='avatar.png')
    slug = models.SlugField(unique=True, blank=True)
    updated_last = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.slug = str(self.username)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username}-{self.updated_last.strftime('%d-%m-%Y')}"

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    body = models.CharField(max_length = 144)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.body}-{self.updated.strftime('%d-%m-%Y')}"


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)