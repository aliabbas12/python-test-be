from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response
    response = exception_handler(exc, context)
    if hasattr(exc, "get_full_details"):
        response.data = exc.get_full_details()
    return response
