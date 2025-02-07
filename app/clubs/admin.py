from django.contrib import admin

from clubs.models import (
    Club,
    ClubMembership,
    Event,
    EventAttendance,
    EventAttendanceLink,
    RecurringEvent,
)
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


class EventAttendanceInlineAdmin(admin.TabularInline):
    """List event attendees in event admin."""

    model = EventAttendance
    extra = 0
    readonly_fields = ("created_at",)


class EventAttendenceLinkInlineAdmin(admin.StackedInline):
    """List event links in event admin."""

    model = EventAttendanceLink
    readonly_fields = (
        "target_url",
        "club",
        "tracking_url_link",
    )
    extra = 0

    def tracking_url_link(self, obj):
        return obj.as_html()


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

    inlines = (EventAttendenceLinkInlineAdmin, EventAttendanceInlineAdmin)


admin.site.register(Club, ClubAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RecurringEvent, RecurringEventAdmin)
