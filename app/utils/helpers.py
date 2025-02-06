from urllib.parse import urljoin
from django.http import HttpRequest
from django.urls import reverse

from app.settings import BASE_URL


def reverse_query(viewname, query=None, **kwargs):
    """Wraps django's reverse function to add query params."""
    query = query if query else {}

    return (
        reverse(viewname, **kwargs)
        + ("?" if len(query.keys()) > 0 else "")
        + "&".join([f"{key}={value}" for key, value in query.items()])
    )


def get_client_ip(request: HttpRequest) -> str:
    """
    Get IP Address from request.

    First checks if the request has an HTTP_X_FORWARDED_FOR header,
    otherwise it will use the default ip header.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


def get_full_url(path: str):
    """Get full url of a sub path using root domain."""

    return urljoin(BASE_URL, path)
