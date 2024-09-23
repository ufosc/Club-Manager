"""
Api Views for core app functionalities.
"""

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import exception_handler

from app.settings import IS_TESTING_MODE
from utils.logging import print_error


def health_check(request):
    """API Health Check."""
    payload = {"status": 200, "message": "Systems operational."}
    return JsonResponse(payload, status=200)


def api_exception_handler(exc, context):
    """Custom exception handler for api."""
    response = exception_handler(exc, context)

    if IS_TESTING_MODE:
        return response

    if response is not None:
        response.data["status_code"] = response.status_code
    else:
        print_error()
        response = Response(
            {"status_code": 400, "detail": str(exc)}, status=HTTP_400_BAD_REQUEST
        )

    return response
