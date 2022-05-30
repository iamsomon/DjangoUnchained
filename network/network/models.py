from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name='followerss', symmetrical=False)
    following = models.ManyToManyField('self', related_name='followingg', symmetrical=False)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name="liked_users")