#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2
import time
import tensorflow as tf 
import numpy as np


# In[2]:


# basic init
# MODEL_PATH=r"AI-Aquaculturing/ForEdgetpuModels/edgetpu_koifish_1000000/koifish_detect-100w.tflite"
# img_path = r"AI-Aquaculturing/101.png"


# In[3]:


def image_preprocess(image, HEIGHT, WIDTH):
    """
    This function is handling that tflite model input_details, and convert image to tflite format.
    
    It will return cv2 image and input_data which mean image was be converted.
    """
    img = image
    if img.any():
        imH, imW, _ = img.shape
        image_resized = cv2.resize(img, (WIDTH, HEIGHT))
        input_data = np.expand_dims(image_resized, axis=0)
    else:
        return False
    return True, input_data, img


# In[4]:


def set_interpreter(image, MODEL_PATH):
    """
    set_interpreter mean you need set_tensor in memory and invoke the interpreter.
    
    this function will return interpreter to doing pridict stuff like, output_details that you can get predicted imformation about detection boxes, scores classes ....
    
    return img data is allow you to save original image.
    
    """
    
    interpreter = tf.lite.Interpreter(MODEL_PATH)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    HEIGHT = input_details[0]['shape'][1]
    WIDTH = input_details[0]['shape'][2]
    
    status, input_data, img = image_preprocess(
        image=image,
        HEIGHT=HEIGHT,
        WIDTH=WIDTH
    )
    
    if status:
        interpreter.allocate_tensors()
        interpreter.set_tensor(input_details[0]['index'],input_data)
        start_time = time.time()
        interpreter.invoke()
        stop_time = time.time()
    else:
        print("maybe your image get some error.")
        
    print("set time is coast:{}".format(stop_time-start_time))
    return interpreter, output_details, img


# In[5]:


def predict(output_details, interpreter):
    return interpreter.get_tensor(output_details[0]['index'])[0], interpreter.get_tensor(output_details[2]['index'])[0]


# In[6]:


def get_predictBox(boxes, scores, img, classes="1"):
    """
    This function help you to draw the detection box on image and counting population for your target.
    """
    Population = int()
    for i in range(len(scores)):
        imH, imW, _ = img.shape
        if (scores[i] > 0.5) and (scores[i] <= 1.0):
            Population = Population + 1
            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()

            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))
            cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
            object_name = classes
            label = '%s: %d%%' % (object_name, int(scores[i]*100))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window

            cv2.rectangle(img, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(img, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
    return img, Population

