
from django.db import models

from image_uploader.backend.constants import Gender


class ImageWithMetadata(models.Model):
    """
    Initial image loaded by an user. It could contain different related crops
    """
    image = models.ImageField()


class Metadata(models.Model):
    """
    In this very case and without more information I've decided to keep going
    with storing the metadata in the DB as it's quite easy to handle and it
    does not involve creating additional files in a manual fashion.

    I've considered so far the next choices:
        1- Storing it as separate hidden files. The code becomes more complex
           as far as every metadata retrieval implies 1 access to DB to get
           the image and it's path and a file reading to get its metadata.

        2- Storing it as actual metadata in the same image file.
           I'm not very familiar with this option, however it seems that there
           are libraries that allow this kind of metadata handling.

        3- Create a new model that keeps a 1-to-1 relation with the image.
           I've chosen this one for simplicity's sake.

    Just one caveat about the pros and cons:
        - The main con is that metadata is separated from the actual data.
        - The main pros is that we've got DB coherence guaranteed and in a
          production env we would also have metadata backup by default as
          every system keeps DB backup images
    """
    # Different attributes we want to store for every single Image
    gender = models.CharField(max_length=1, choices=Gender.choices)

    def serialize(self):
        value_to_label_map = dict(zip(Gender.values, Gender.labels))
        return {
            'gender': (self.gender, value_to_label_map.get(self.gender))
        }


class ImageRegion(models.Model):
    """
    Different crops saved from an image.
    Every single crop holds:
        - The image itself
        - The source image used to take the crop
        - Metadata related with this crop
    """
    # This image is intended to be the crops of any image
    image = models.ImageField()

    # If the source image is dropped. All its regions need to be dropped to!
    src_image = models.ForeignKey(ImageWithMetadata, on_delete=models.CASCADE)

    # The deletion flow should be deleting an image ( that should be bound
    # to a customer) triggers the metadata deletion. No metadata deletion
    # should occur if its image is still alive.
    metadata = models.OneToOneField(Metadata, on_delete=models.PROTECT)

    def serialize(self, uri_builder=None):
        def by_pass_uri(uri):
            return uri
        uri_builder = uri_builder or by_pass_uri

        return {
            'id': self.id,
            'image': uri_builder(self.image.url),
            'metadata': self.metadata.serialize()
        }
