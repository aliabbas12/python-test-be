import collections
import typing

import inflection
import six
from rest_framework.renderers import JSONRenderer

__all__ = ["CamelCaseJSONRenderer"]


def snake_to_camel(data: typing.Any):
    if isinstance(data, dict):
        return {
            inflection.camelize(k, False)
            if k and isinstance(k, six.string_types) and not k.isupper()
            else k: snake_to_camel(v)
            for k, v in data.items()
        }
    if isinstance(data, collections.Iterable) and not isinstance(
        data, six.string_types
    ):
        return [snake_to_camel(item) for item in data]
    return data


class CamelCaseJSONRenderer(JSONRenderer):
    """
    partially taken from https://github.com/vbabiy/djangorestframework-camel-case
    """

    def render(self, data, *args, **kwargs):
        return super().render(snake_to_camel(data), *args, **kwargs)
