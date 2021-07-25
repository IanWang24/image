from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from .utils import detect,yolo_detect
import cv2

from tqdm import tqdm


import time
import tensorflow as tf

from statistics import mean
from tensorflow.python.saved_model import tag_constants
from tensorflow.compat.v1 import InteractiveSession


pb_path = r"imageupload/checkpoints/yolov4-416"
saved_model_loaded = tf.saved_model.load(pb_path, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']


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
        original_image = cv_obj_img
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)


        image_data = cv2.resize(original_image, (416, 416))
        image_data = image_data / 255.


        images_data = []
        for i in range(1):
            images_data.append(image_data)
        images_data = np.asarray(images_data).astype(np.float32)


        batch_data = tf.constant(images_data)
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]
        boxes, scores, _, _ = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=0.45,
            score_threshold=0.60
        )

        imH, imW, _ = original_image.shape
        original_image = cv_obj_img

        count = 0
        for i in tqdm(range(len(scores[0]))):


            if scores[0][i] > 0:
                count+=1
                # init content
                fontScale = 0.4
                object_name = "fish"
                score = scores[0][i]
                box = boxes[0][i]


                ymin = int(box[0] * imH)
                ymax = int(box[2] * imH)
                xmin = int(box[1] * imW)
                xmax = int(box[3] * imW)

                bbox_thick = int(0.6 * (imH + imW) / 600)

                cv2.rectangle(original_image, (xmin,ymin), (xmax,ymax), (10, 255, 0), bbox_thick)

                label = '%s: %d%%' % ("fish", int(score*100))
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, fontScale, bbox_thick) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window

                cv2.rectangle(original_image, (xmin, label_ymin-labelSize[1]-5), (xmin+labelSize[0], label_ymin+baseLine-5), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(original_image, label, (xmin, label_ymin-2), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 0), bbox_thick) # Draw label text
        # cv_obj_img1 = cv_obj_img
        # cv_obj_img = cv2.resize(cv_obj_img, (416, 416))
        # batch_data = yolo_detect.process_data(cv_obj_img)
        # pred_bbox = infer(batch_data)
        # for key, value in pred_bbox.items():
        #     boxes = value[:, :, 0:4]
        #     pred_conf = value[:, :, 4:]
        #
        # boxes, scores, _, _ = tf.image.combined_non_max_suppression(
        #     boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        #     scores=tf.reshape(
        #         pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        #     max_output_size_per_class=50,
        #     max_total_size=50,
        #     iou_threshold=0.45,
        #     score_threshold=0.70
        # )
        #
        # img_tmp, c_tmp = yolo_detect.draw_bbox(boxes, scores, cv_obj_img, cv_obj_img1)

        self.quantity = count
        #
        img = Image.fromarray(original_image)
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        img_png = buffer.getvalue()

        self.after_predict.save("predict image name:\t" + str(self.image) , ContentFile(img_png), save=False)

        super().save(*args, **kwargs)


class Video(models.Model):
    caption=models.CharField(max_length=100)
    video=models.FileField(upload_to="video/")
    after_predict =models.FileField(upload_to='predict_video/')
    quantity = models.IntegerField(blank=False, default=0)

    def save(self, *args, **kwargs):

        self.after_predict.save("predict video name:\t" + str(self.video)+".mp4" , ContentFile(img_png), save=False)






        super().save(*args, **kwargs)
