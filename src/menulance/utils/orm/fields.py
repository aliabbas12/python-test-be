import json
from abc import abstractmethod, ABCMeta
from dataclasses import asdict

from django.db import models


class DataClassJsonField(models.JSONField, metaclass=ABCMeta):
    @property
    @abstractmethod
    def data_class(self):
        pass

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.data_class(**json.loads(value))

    def to_python(self, value):
        if isinstance(value, self.data_class):
            return value

        if value is None:
            return value

        return self.data_class(**value)

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, self.data_class):
            return super().get_prep_value(asdict(value))
        return super().get_prep_value(value)
