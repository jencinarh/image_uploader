from django.urls import path

from image_uploader.backend.api import upload, crop

urlpatterns = [
    path('upload-image', upload),
    path('crop-image', crop),
]
