from django.contrib import admin
from .models import User, Post, UserFollowing

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['body', 'author', 'publish']


admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(UserFollowing)
