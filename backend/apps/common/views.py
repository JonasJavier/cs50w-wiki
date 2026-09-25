"""Operational endpoints."""

from django.http import JsonResponse


def health_check(request):
    """Simple liveness probe.

    This endpoint intentionally avoids DRF, throttling, cache, Redis and
    database access so platform health checks can verify the web process itself.
    """
    return JsonResponse({"status": "ok"})
