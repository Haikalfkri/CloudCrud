import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

ERROR_CODES = {
    400: "validation_error",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
}


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Exception yang tidak dikenali DRF -> 500 dalam format yang sama
    if response is None:
        logger.error("Unhandled exception", exc_info=exc)
        return Response(
            {"error": {"code": "server_error", "message": "Internal server error.", "details": None}},
            status=500,
        )

    if response.status_code == 400:
        message, details = "Invalid request data.", response.data
    else:
        message = response.data.get("detail", "Request failed.") if isinstance(response.data, dict) else "Request failed."
        details = None

    response.data = {
        "error": {
            "code": ERROR_CODES.get(response.status_code, "error"),
            "message": str(message),
            "details": details,
        }
    }
    return response