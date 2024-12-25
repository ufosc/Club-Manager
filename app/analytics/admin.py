from django.contrib import admin
from django.utils.safestring import mark_safe
from utils.admin import other_info_fields
from django.utils.translation import gettext_lazy as _


class QRCodeAdmin(admin.ModelAdmin):
    """Admin config for QR Codes."""

    readonly_fields = (
        "created_at",
        "updated_at",
        "size",
        "preview",
    )

    fieldsets = (
        (
            None,
            {
                "fields": ("preview", "image"),
            },
        ),
        (
            _("Details"),
            {"fields": ("size", "url")},
        ),
        other_info_fields,
    )

    def preview(self, obj):
        if not obj.image:
            return None

        return mark_safe(
            "<svg width='90' height='90' style='background-color:white'>"
            f"<image  xlink:href={obj.image.url} width='100%'>"
            "</svg>"
        )
