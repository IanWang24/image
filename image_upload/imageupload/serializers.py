from rest_framework import serializers
from .models import UploadImage


class MyFileSerializer(serializers.ModelSerializer):
    class Meta():
        model=UploadImage
        fields = ('image', 'description', 'uploaded_at',)
