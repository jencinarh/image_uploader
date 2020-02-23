from PIL import Image

# Typing
from django.http import HttpRequest, HttpResponse, JsonResponse


def _crop_image(url, x, y, width, height):
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
    return pil_image.crop((x, y, x + width, y + height))


def _create_crop(img_id, coords, metadata):
    """
    Create a crop for the given image.
    That crop is defined by coords and have to store the metadata information

    :param img_id:
    :param coords:
    :param metadata:
    :return:
    """
    # Business code; Crop the source image using the passed coordinates
    from image_uploader.backend.models import ImageWithMetadata
    img = ImageWithMetadata.objects.get(id=img_id)

    crop = _crop_image(
        img.image.url,
        coords['x'],
        coords['y'],
        coords['width'],
        coords['height']
    )

    # Now that we've got a crop we can create all the instances in DB
    from image_uploader.backend.models import Metadata
    metadata = Metadata.objects.create(gender=metadata.get('gender'))

    from image_uploader.backend.models import ImageRegion
    image_region = ImageRegion.objects.create(
        image=crop,
        src_image=img,
        metadata=metadata
    )
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
    # TODO Create the in-memory file

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


def crop(request: HttpRequest) -> HttpResponse:
    """
    Crop the requested image and save a bound image with its metadata to the
    src image

    :param request:
    :return:
    """
    # This should hold some kind of param validation.
    # For this snippet we'll assume that this input is correct
    img_id = request.POST.get('id')
    coords = request.POST.get('coords')
    metadata = request.POST.get('metadata')

    image_region = _create_crop(img_id, coords, metadata)

    response = {
        "id": image_region.id,
        "srcImage": img_id,

    }
    return JsonResponse(
        response,
        status=200
    )
