from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from imageupload.views import  post,display_images,delete



urlpatterns = [
    url(r'^upload/',post, name='file-upload'),
    url(r'^display/',display_images, name='display'),
    path('admin/', admin.site.urls),
    url(r'^delete/(?P<pk>[0-9]+)/$', delete, name='delete')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT )
