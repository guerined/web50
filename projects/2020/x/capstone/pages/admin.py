from django.contrib import admin
from .models import User, QRCode

# Register your models here.
admin.site.register(User)
admin.site.register(QRCode)
