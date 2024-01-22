from abc import abstractmethod, ABCMeta
from dataclasses import asdict

from pydantic import ValidationError
from rest_framework import serializers
from rest_framework.fields import JSONField


class DataClassJsonField(JSONField, metaclass=ABCMeta):
    """To store dataclass as JSON. May not be needed"""

    @property
    @abstractmethod
    def dataclass(self):
        pass

    @property
    @abstractmethod
    def data_class_error_messages(self):
        pass

    def to_internal_value(self, data):
        value = super(DataClassJsonField, self).to_internal_value(data)
        try:
            return self.dataclass(**value)
        except (TypeError, ValidationError) as exc:
            raise serializers.ValidationError(
                "{}. Detail: {}".format(self.data_class_error_messages["invalid"], exc),
                code="invalid",
            )

    def to_representation(self, value):
        return super().to_representation(asdict(value))
