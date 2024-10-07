import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible


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


def get_or_none(model: models.Model, query=dict, fail_silently=False, **kwargs):
    """Return object if found, None otherwise."""
    try:
        objects = model.objects.filter(**query, **kwargs)

        if objects.exists() and objects.count() == 1:
            return objects.first()
        elif objects.count() > 1:
            if fail_silently:
                return None

            raise model.MultipleObjectsReturned()
        else:
            return None
    except Exception:
        # print_error()
        return None
