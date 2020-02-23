from django.urls import path

from image_uploader.backend.api import upload, crop, get_images

urlpatterns = [
    path('upload-image', upload),
    path('crop-image', crop),
    path('get-images', get_images),
]
