from django.contrib import admin

# Register your models here.
from .models import Post, User
#register both models into django admin page
admin.site.register(Post)
admin.site.register(User)


