from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        default="profile_pics/default.jpg",
        blank=True,
        null=True
    )

    # Users who follow this user
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True
    )

    def __str__(self):
        return self.username

    # Optional helper to get users this user is following
    def get_following(self):
        return self.following.all()
