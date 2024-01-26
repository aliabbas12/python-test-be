import typing
import uuid
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from io import BytesIO

import inflection
import six
from PIL import Image
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, JSONParser

__all__ = [
    "CamelCaseJSONParser",
    "RandomFilenameImageFileUploadParser",
    "ImageFileUploadParser",
]


def camel_to_snake(data: typing.Any):
    if isinstance(data, dict):
        return {
            inflection.underscore(k)
            if isinstance(k, six.string_types)
            else k: camel_to_snake(v)
            for k, v in data.items()
        }
    if isinstance(data, Iterable) and not isinstance(
            data, six.string_types
    ):
        return [camel_to_snake(item) for item in data]
    return data


class CamelCaseJSONParser(JSONParser):
    """
    partially taken from https://github.com/vbabiy/djangorestframework-camel-case
    """

    def parse(self, *args, **kwargs):
        return camel_to_snake(super().parse(*args, **kwargs))


class QueryParameterParser(metaclass=ABCMeta):
    """Parser for GET parameter parsing"""

    @abstractmethod
    def parse(self, data):
        pass


class CamelCaseJSONQueryParameterParser(QueryParameterParser):
    def parse(self, data):
        return camel_to_snake(data)


class ImageFileUploadParser(FileUploadParser):
    media_type = "image/*"


class RandomFilenameImageFileUploadParser(ImageFileUploadParser):
    """
    FileUploadParser that allows only image file uploads and does not
    force a filename to be present in HTTP_CONTENT_DISPOSITION header
    """

    errors = {
        "no_image": "Corrupted image or not an image at all.",
    }

    def parse(self, *args, **kwargs):
        data = super().parse(*args, **kwargs)
        file = BytesIO(data.files["file"].read())
        try:
            image = Image.open(file)
            image.verify()
            data.files["file"].image = image
            data.files["file"].content_type = Image.MIME.get(image.format)
            data.files["file"].name += ".{}".format(image.format.lower())
        except Exception:
            # Pillow doesn't recognize it as an image.
            raise ParseError(self.errors["no_image"])
        if hasattr(data.files["file"], "seek") and callable(data.files["file"].seek):
            data.files["file"].seek(0)

        return data

    def get_filename(self, *args, **kwargs):
        return str(uuid.uuid4())
