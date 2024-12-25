from django.contrib import admin


from clubs.models import Club, ClubMembership, Event, RecurringEvent
from clubs.services import ClubService


class ClubMembershipInlineAdmin(admin.StackedInline):
    """Create club memberships in admin."""

    model = ClubMembership
    extra = 1


class ClubAdmin(admin.ModelAdmin):
    """Admin config for Clubs."""

    inlines = (ClubMembershipInlineAdmin,)
    list_display = (
        "name",
        "id",
        "members_count",
        "created_at",
    )

    def members_count(self, obj):
        return obj.memberships.count()


class RecurringEventAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "day",
        "location",
        "start_date",
        "end_date",
    )
    actions = ("sync_events",)

    @admin.action(description="Sync Events")
    def sync_events(self, request, queryset):

        for recurring in queryset.all():
            ClubService.sync_recurring_event(recurring)

        return


class EventAdmin(admin.ModelAdmin):
    """Admin config for club events."""

    list_display = (
        "__str__",
        "id",
        "location",
        "start_at",
        "end_at",
    )
    ordering = ("start_at",)


# class QRCodeAdmin(admin.ModelAdmin):
#     """Admin config for QR Codes."""

#     readonly_fields = (
#         "created_at",
#         "updated_at",
#         "size",
#         "preview",
#     )

#     fieldsets = (
#         (
#             None,
#             {
#                 "fields": ("preview", "image"),
#             },
#         ),
#         (
#             _("Details"),
#             {"fields": ("size", "url")},
#         ),
#         other_info_fields,
#     )

#     def preview(self, obj):
#         if not obj.image:
#             return None

#         return mark_safe(
#             "<svg width='90' height='90' style='background-color:white'>"
#             f"<image  xlink:href={obj.image.url} width='100%'>"
#             "</svg>"
#         )


admin.site.register(Club, ClubAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RecurringEvent, RecurringEventAdmin)
# admin.site.register(QRCode, QRCodeAdmin)
