import json
import os
import sys
import time
from io import BytesIO

from PIL import Image
# Typing
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, HttpResponse, JsonResponse

from image_uploader.backend.models import ImageRegion
from image_uploader.backend.models import ImageWithMetadata
from image_uploader.backend.models import Metadata


def _crop_image(url, x, y, x2, y2):
    """
    Use PIL to crop the given subimage
    :param url:
    :param x:
    :param y:
    :param width:
    :param height:
    :return:
    """
    pil_image = Image.open(url)
    return pil_image.crop((x, y, x2, y2))


def _create_crop(img, coords, metadata):
    """
    Create a crop for the given image.
    That crop is defined by coords and have to store the metadata information

    :param img:
    :param coords:
    :param metadata:
    :return:
    """
    print(coords)
    crop = _crop_image(
        img.image.path,
        coords['x'],
        coords['y'],
        coords['x2'],
        coords['y2']
    )

    tmp = BytesIO()
    crop.save(tmp, format='PNG')  # loseless format
    new_name = "{}_{}{}".format(
        img.image.name,
        time.time(),
        '.png'
    )

    in_memory_crop = InMemoryUploadedFile(
        tmp,
        None,
        new_name,
        'image/png',
        sys.getsizeof(tmp),
        None
    )
    # Now that we've got a crop we can create all the instances in DB
    metadata = Metadata.objects.create(gender=metadata.get('gender'))
    image_region = ImageRegion.objects.create(
        image=in_memory_crop,
        src_image=img,
        metadata=metadata
    )
    image_region.save()
    return image_region


# Api function-like views
def upload(request: HttpRequest) -> HttpResponse:
    """
    Upload an image and save it to DB.
    This could be improved by separating the business code from the api and
    DB code.
    However, this is a quick snippet.

    :param request:
    :return:
    """
    f = request.FILES['file']

    # Create an image with no crops in there
    from image_uploader.backend.models import ImageWithMetadata
    img = ImageWithMetadata.objects.create(
        image=f
    )

    response = {
        "id": img.id
    }
    return JsonResponse(
        response,
        status=200
    )


def crop(request: HttpRequest) -> JsonResponse:
    """
    Crop the requested image and save a bound image with its metadata to the
    src image

    :param request:
    :return:
    """

    post_data = json.loads(request.body)
    print(post_data)
    # This should hold some kind of param validation.
    # For this snippet we'll assume that this input is correct
    img_id = post_data.get('id')
    coords = post_data.get('coords')
    metadata = post_data.get('metadata', {})

    img = ImageWithMetadata.objects.get(id=img_id)
    image_region = _create_crop(img, coords, metadata)

    response = {
        "id": image_region.id,
        "srcImage": img_id,

    }
    return JsonResponse(
        response,
        status=200
    )


def get_images(request: HttpRequest) -> JsonResponse:
    """
    Get all the images to list them and its crops in the website
    :param request:
    :return:
    """
    qs = ImageWithMetadata.objects.prefetch_related(
        "imageregion_set",
        "imageregion_set__metadata"
    )

    response = {
        "images": None
    }
    images = []
    for image in qs:
        serialized_image = {
            "id": image.id,
            "image": request.build_absolute_uri(image.image.url),
            "crops": [
                crop_instance.serialize(uri_builder=request.build_absolute_uri)
                for crop_instance in image.imageregion_set.all()
            ]
        }
        images.append(serialized_image)

    response['images'] = images
    return JsonResponse(
        response,
        status=200
    )