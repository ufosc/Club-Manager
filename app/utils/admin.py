from django.utils.translation import gettext_lazy as _

other_info_fields = (
    (
        (
            _("Other Information"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    .__iter__()
    .__next__()
)

__all__ = ("other_info_fields",)
