from django.http import HttpRequest
from django.urls import reverse


def reverse_query(viewname, query=None, **kwargs):
    """Wraps django's reverse function to add query params."""
    query = query if query else {}

    return (
        reverse(viewname, **kwargs)
        + ("?" if len(query.keys()) > 0 else "")
        + "&".join([f"{key}={value}" for key, value in query.items()])
    )


def clean_list(target: list):
    """Remove None values and empty strings from list."""

    return [item for item in target if item is not None and item != ""]


def str_to_list(target: str | None):
    """Split string into list using comma as a separator."""
    if not isinstance(target, str):
        return []

    items = target.split(",")
    items = clean_list([item.strip() for item in items])

    return items


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
