from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Conflicted state.")
    default_code = "conflict"


class ConflictWithExtraData(Conflict):
    """In case default Exceptions are not able to detect a problem and extra data is needed"""

    def __init__(self, extra_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_data = extra_data

    def _get_full_details(self, detail):
        if isinstance(detail, list):
            return [self._get_full_details(item) for item in detail]
        elif isinstance(detail, dict):
            return {key: self._get_full_details(value) for key, value in detail.items()}
        return {"message": detail, "code": detail.code, "extra_data": self.extra_data}

    def get_full_details(self):
        return self._get_full_details(self.detail)
