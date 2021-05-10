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






from .models import UploadImage
from .serializers import MyFileSerializer


def post(request):
	url = {}
	if request.method =="POST":

		fs = FileSystemStorage()
		file = request.FILES["image"]
		content = request.POST["description"]
		document = UploadImage.objects.create(image = file , description = content)
		# print("C:/Users/Ian/Desktop/api/upload_media/" + str(document.image))
		# file = "C:/Users/Ian/Desktop/api/upload_media/" + str(document.image)
		# img_gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
		# filename = "C:/Users/Ian/Desktop/api/result/"+str(document.image)
		# print(filename)
		# cv2.imwrite(filename ,img_gray)
		# result.save()
		# img = cv2.imread('document.')
		url['url'] = fs.url(document.image)
		# print("C:/Users/Ian/Desktop/api/upload_media/" + str(document.image))
		# cv2.imshow('My Image',img_gray)
	return render(request,"upload.html",url)

def display_images(request):
	allimages = UploadImage.objects.all()
	# model -> process -> save_to_result ->
	return render(request, 'display.html', {'images' : allimages})


def delete (request, pk):
	img = get_object_or_404(UploadImage, pk=pk)  # Get your current cat
	if request.method == 'POST':  # If method is POST,
		img.delete()                     # delete the cat.
		return redirect('http://127.0.0.1:8000/display/')             # Finally, redirect to the homepage.
	return render(request, 'delete_view.html', {'img': img})








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
