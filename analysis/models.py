from django.db import models
from account.models import User
import os

# Create your models here.


class UserFiles(models.Model):
    file_name = models.CharField(max_length=100, verbose_name='نام فایل')
    file = models.FileField(upload_to='excels/', verbose_name='فایل')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.file}'
    
    class Meta:
        verbose_name = 'فایل کاربر'
        verbose_name_plural = 'فایل های کاربران'