from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=30, verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوا')
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey(to=User, related_name='articles', on_delete=models.CASCADE)
