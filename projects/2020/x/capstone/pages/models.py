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
    ENCRYPTION_TYPE_CHOICES = [
        ('WEP', 'WEP'),
        ('WPA', 'WPA'),
        ('WPA2-EAP', 'WPA2-EAP'),
        ('no pass', 'no pass'),
    ]

    QR_STYLE_CHOICES = [
        ('style1', 'Style 1'),
        ('style2', 'Style 2'),
        ('style3', 'Style 3'),
        ('style4', 'Style 4'),
    ]

    FRAME_STYLE_CHOICES = [
        ('frame1', 'Frame 1'),
        ('frame2', 'Frame 2'),
        ('frame3', 'Frame 3'),
        ('frame4', 'Frame 4'),
    ]

    YES_NO_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    name = models.CharField(max_length=255, default='QR Code')
    network_name = models.CharField(max_length=255, blank=True)
    network_password = models.CharField(max_length=255, blank=True)
    encryption_type = models.CharField(
        max_length=8, choices=ENCRYPTION_TYPE_CHOICES, blank=True)
    hidden_network = models.BooleanField(default=False)
    qr_style = models.CharField(
        max_length=6, choices=QR_STYLE_CHOICES, blank=True)
    frame_style = models.CharField(
        max_length=6, choices=FRAME_STYLE_CHOICES, blank=True)
    border = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    background = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    border_color = models.CharField(max_length=7, blank=True)  # Hex color code
    background_color = models.CharField(
        max_length=7, blank=True)  # Hex color code
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qrcodes/')
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    short_url = models.CharField(max_length=10, blank=True, null=True)
    times_scanned = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.user.username + ' - ' + self.name + str(self.created_at)
