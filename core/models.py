import uuid
import os
from django.db import models
from django.contrib.auth.models import User

def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1] 
    filename = f"{uuid.uuid4()}.{ext}" 
    return os.path.join('avatars/', filename)

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, verbose_name="Никнейм")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'