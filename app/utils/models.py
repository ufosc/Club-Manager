import os
import uuid

from django.core import exceptions
from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.utils.deconstruct import deconstructible
from rest_framework.fields import ObjectDoesNotExist

from utils.types import T

# from utils.types import T


@deconstructible
class UploadFilepathFactory(object):
    """
    Create function for model FileField to rename file and upload to a path.

    Parameters
    ----------
        path (str): Nested directory name in /media/uploads/ folder where the file will be uploaded.
            Ex: "/user/profile/" -> "/media/uploads/user/profile/"
    """

    def __init__(self, path: str):
        self.path = path

    def __call__(self, instance, filename):
        extension = filename.split(".")[-1]
        filename = "{}.{}".format(uuid.uuid4().hex, extension)

        nested_dirs = [dirname for dirname in self.path.split("/") if dirname]
        return os.path.join("uploads", *nested_dirs, filename)


def get_or_none(model: models.Model, fail_silently=True, **kwargs):
    """Return object if found, None otherwise."""
    try:
        object = model.objects.get(**kwargs)
        return object
    except exceptions.MultipleObjectsReturned as e:
        if fail_silently:
            return None
        else:
            raise e
    except Exception:
        return None


class ReverseOneToOneOrNoneDescriptor(ReverseOneToOneDescriptor):
    def __get__(self, instance, cls=None):
        try:
            return super(ReverseOneToOneOrNoneDescriptor, self).__get__(
                instance=instance, cls=cls
            )
        except ObjectDoesNotExist:
            return None


class OneToOneOrNoneField(models.OneToOneField[T]):
    """
    A OneToOneField that returns None if the related object doesn't exist.

    Source: <https://stackoverflow.com/questions/3955093/django-return-none-from-onetoonefield-if-related-object-doesnt-exist
    """  # noqa: E501

    related_accessor_class = ReverseOneToOneOrNoneDescriptor
