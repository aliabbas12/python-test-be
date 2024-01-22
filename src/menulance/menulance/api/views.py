from django.http import JsonResponse
from rest_framework import status


def not_found(*args, **kwargs):
    data = {"error": "Not Found (404)"}
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


def permission_denied(*args, **kwargs):
    data = {"error": "Forbidden (403)"}
    return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
