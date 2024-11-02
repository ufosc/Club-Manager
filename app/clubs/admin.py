from django.contrib import admin


from clubs.models import Club, ClubMembership, Event, QRCode, RecurringEvent


class ClubMembershipInlineAdmin(admin.StackedInline):
    """Create club memberships in admin."""

    model = ClubMembership
    extra = 1


class ClubAdmin(admin.ModelAdmin):
    """Admin config for Clubs."""

    inlines = [ClubMembershipInlineAdmin]
    list_display = ["name", "id", "members_count", "created_at"]

    def members_count(self, obj):
        return obj.memberships.count()


class RecurringEventAdmin(admin.ModelAdmin):

    list_display = ["__str__", "day", "location", "start_date", "end_date"]
    actions = ["sync_events"]

    @admin.action(description="Sync Events")
    def sync_events(self, request, queryset):

        for recurring in queryset.all():
            recurring.sync_events()

        return


class EventAdmin(admin.ModelAdmin):
    """Admin config for club events."""

    list_display = ["__str__", "id", "location", "event_start", "event_end"]
    ordering = ["event_start"]


admin.site.register(Club, ClubAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RecurringEvent, RecurringEventAdmin)
admin.site.register(QRCode)
