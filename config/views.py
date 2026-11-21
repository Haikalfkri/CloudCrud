import logging

from django.db import OperationalError, connection
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@extend_schema(exclude=True)
@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})

@extend_schema(exclude=True)
@api_view(["GET"])
def health_live(request):
    return Response({"status": "alive"})

@extend_schema(exclude=True)
@api_view(["GET"])
def health_ready(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except OperationalError:
        logger.exception("Readiness check failed: database unreachable")
        return Response(
            {"status": "unavailable", "database": "down"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return Response({"status": "ready", "database": "up"})