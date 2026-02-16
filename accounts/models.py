from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    # files will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.id}/{filename}'


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to=user_directory_path, default='defaults/default_profile.png', blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
