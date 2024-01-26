import pytz
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.django_overrides import get_user_model


class MenulanceJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Activating the user defined timezone is crucial for the analysis stuff (for datetime time
        # truncation, e.g. time casting or flooring by interval). There is no other way for effecting the
        # time zone for those operations.
        # As a "side effect" all serialized date times returned by the server are in the
        # activated timezone (which should actually not pose a problem since date times are
        # returned as an "absolute" point in time - that is - they are serialized in ISO 8601 format
        # containing the time zone designator).
        # Additionally, all date times send to the server are made aware with the activated timezone (which
        # should not pose any problem either).
        if validated_token["tz"]:
            timezone.activate(pytz.timezone(validated_token["tz"]))

        # Use LazyUser and accept that a user that is deactivated or deleted can still access the API
        # as long as the access token is not expired.
        return get_user_model().objects.get(pk=validated_token["uid"])
