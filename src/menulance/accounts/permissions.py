from django.conf import settings
from rest_framework.permissions import BasePermission


def is_superuser(request):
    """Add this function to all new permission models so the Super User can do anything"""
    return hasattr(request, "user") and request.user.is_superuser


class AllowAny(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty permission_classes list,
    but it's useful because it makes the intention more explicit.
    """

    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated clients.
    """

    def has_permission(self, request, view):
        return request.auth is not None or is_superuser(request)


class IsAuthenticatedUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return (
            request.auth
            and hasattr(request.user, "is_anonymous")
            and not request.user.is_anonymous
        ) or is_superuser(request)


class IsAuthenticatedUserTheObjectCreator(IsAuthenticatedUser):
    def has_object_permission(self, request, view, obj):
        creator = getattr(obj, settings.CREATOR_ATTRIBUTE_NAME, None)
        return (creator and creator.id == request.user.id) or is_superuser(request)


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return request.auth and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


# TODO: A django permissions evaluator as well if needed
# class HasPermissions(BasePermission):
#     """
#     Allows access only to clients with provided permissions.
#     """
#
#     pass
