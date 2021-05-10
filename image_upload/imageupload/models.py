from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from .utils import detect
import cv2





class UploadImage(models.Model):
    image = models.FileField(upload_to='upload/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    after_predict =models.FileField(upload_to='predict_image/')
    quantity = models.IntegerField(blank=False, default=0)

    # def __str__(self):
    #     return self.contain_image.name + "predict quantity:{}".format(self.quantity)

    def save(self, *args, **kwargs):

        img = Image.open(self.image)
        cv_obj_img = np.array(img)
        model_path = r"imageupload/tflite_models/koifish_detect-100w.tflite"
        interpreter, output_details, cv_obj_img = detect.set_interpreter(
            image=cv_obj_img,
            MODEL_PATH=model_path
        )

        boxes, scores = detect.predict(output_details, interpreter)

        img_withBox, Population = detect.get_predictBox(boxes, scores, cv_obj_img, classes="koi_fish")

        img = Image.fromarray(img_withBox)

        self.quantity = Population

        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        img_png = buffer.getvalue()
        self.after_predict.save("predict image name:\t" + str(self.image) + ".jpg", ContentFile(img_png), save=False)

        super().save(*args, **kwargs)
