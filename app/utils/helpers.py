from django.urls import reverse


def reverse_query(viewname, query=dict, **kwargs):
    """Wraps django's reverse function to add query params."""
    return (
        reverse(viewname, **kwargs)
        + ("?" if len(query.keys()) > 0 else "")
        + "&".join([f"{key}={value}" for key, value in query.items()])
    )
