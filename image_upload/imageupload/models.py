from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from .core.utils import detect,vid_detect,load_model
import cv2

from tqdm import tqdm


import time
import tensorflow as tf

from statistics import mean
from tensorflow.python.saved_model import tag_constants
from tensorflow.compat.v1 import InteractiveSession




class UploadImage(models.Model):
    image = models.FileField(upload_to='upload/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    after_predict =models.FileField(upload_to='predict_image/video')
    quantity = models.IntegerField(blank=False, default=0)


    def save(self, *args, **kwargs):

        img = Image.open(self.image)
        cv_obj_img = np.array(img)
        original_image = cv_obj_img[:, :, ::-1].copy()

        image_data = cv2.resize(original_image, (416, 416))


        count, image = detect(image_data, infer)

        self.quantity = count
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)

        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        img_png = buffer.getvalue()

        self.after_predict.save("predict image name:\t" + str(self.image) , ContentFile(img_png), save=False)

        super().save(*args, **kwargs)


class Video(models.Model):
    caption=models.CharField(max_length=100)
    video=models.FileField(upload_to="video/")
    after_predict =models.FileField(upload_to='predict_video/video/')
    quantity = models.IntegerField(blank=False, default=0)

    # def save(self, *args, **kwargs):
    #     count = vid_detect(
    #             r'upload_media/videos/{}'.format(self.video),
    #             r'upload_media/predict_video/output_{}'.format(request.FILES["video"]),
    #             infer
    #         )
    # super().save(*args, **kwargs)
