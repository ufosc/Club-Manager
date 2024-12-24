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
