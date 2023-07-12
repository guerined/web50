from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, default='avatar.png')
    updated_last = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class QRCode(models.Model):
    name = models.CharField(max_length=255, default='QR Code')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qrcodes/')
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    short_url = models.CharField(max_length=10, blank=True, null=True)
    times_scanned = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.user.username + ' - ' + self.name + str(self.created_at)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name