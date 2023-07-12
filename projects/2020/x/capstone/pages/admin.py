from django.contrib import admin
from .models import User, QRCode, Contact

# Register your models here.
admin.site.register(User)
admin.site.register(QRCode)
admin.site.register(Contact)