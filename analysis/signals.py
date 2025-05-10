from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import UserFiles
import os

@receiver(post_delete, sender=UserFiles)
def delete_file_on_model_delete(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)