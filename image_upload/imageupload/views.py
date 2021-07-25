from django.shortcuts import render,get_object_or_404,redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.core.files.base import ContentFile

import cv2
import time
import tensorflow as tf

from tqdm import tqdm
from .core.utils import detect,vid_detect,load_model

from statistics import mean
from tensorflow.python.saved_model import tag_constants
from tensorflow.compat.v1 import InteractiveSession



from .models import UploadImage,Video
from .serializers import MyFileSerializer
from .core.utils import detect,vid_detect,load_model

pb_path = r"imageupload/checkpoints/yolov4-416"
saved_model_loaded = tf.saved_model.load(pb_path, tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']

def post(request):
	url = {}
	pred_url = {}
	content={}
	last = UploadImage.objects.last()
	if request.method =="POST":
		fs = FileSystemStorage()
		file = request.FILES["image"]
		content = request.POST["description"]
		document = UploadImage.objects.create(image = file , description = content)
		url['url'] = fs.url(document.image)
		pred_url['url']=fs.url(document.after_predict)
		last = UploadImage.objects.last()

	return render(request,"upload.html" ,{'img' :last})

def display_images(request):
	allvideo = Video.objects.all()
	# model -> process -> save_to_result ->
	return render(request, 'display.html', {'videos' : allvideo})


def delete (request, pk):
	img = get_object_or_404(UploadImage, pk=pk)  # Get your current cat
	if request.method == 'POST':  # If method is POST,
		img.delete()                     # delete the cat.
		return redirect('http://127.0.0.1:8000/display/')             # Finally, redirect to the homepage.
	return render(request, 'delete_view.html', {'img': img})

def post_video (request):
	if request.method =="POST":
		file= request.FILES["video"]
		content = request.POST["caption"]
		document = Video.objects.create(video = file , caption = content)
		last = Video.objects.last()
		count = vid_detect(
				r'../upload_media/{}'.format(last.video.name),
				r'../upload_media/predict_video/{}'.format(last.video.name),
				infer
			)
		c = mean(count)
		video_path = r'predict_video/{}'.format(last.video.name)
		print(video_path)
		last.after_predict = video_path
		last.quantity = int(c)
		last.save()
	all = Video.objects.last()


	return render(request,"uploadvideo.html",{'video': all})









# def post(request):
#     if request.method == 'POST':
#         student = MyFileSerializer(request.POST, request.FILES)
#         if student.is_valid():
#             handle_uploaded_file(request.FILES['image'])
#             return HttpResponse("File uploaded successfuly")
#     else:
#         student = MyFileSerializer()
#     return render(request,"upload.html",{'form':student})


# class MyFileView(APIView):
# 		# MultiPartParser AND FormParser
# 		# https://www.django-rest-framework.org/api-guide/parsers/#multipartparser
# 		# "You will typically want to use both FormParser and MultiPartParser
# 		# together in order to fully support HTML form data."
# 		parser_classes = (MultiPartParser, FormParser)
# 		def post(self, request, *args, **kwargs):
# 				file_serializer = MyFileSerializer(data=request.data)
# 				if file_serializer.is_valid():
# 						file_serializer.save()
# 						return Response(file_serializer.data, status=status.HTTP_201_CREATED)
# 				else:
# 						return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 				return render(request,"upload.html",{'form':student})















# @api_view(['GET', 'POST'])
#
# def image_GET(request):
#     if request.method == 'GET':
#         serializer = image_GET_Serializer(snippets, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
# def image_POST(request):
#     if request.method == 'POST':
#         upload_file = request.FILES['image']
#
#
#

    #     serializer = image_POST_Serializer(data=request.data)
    # elif serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
