from django.db import models
from django.contrib.auth.models import User

class UploadImage(models.Model):
    image = models.FileField(upload_to='upload/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
