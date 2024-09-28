from django.contrib import admin

from clubs.models import Club, ClubMembership


class ClubMembershipInlineAdmin(admin.StackedInline):
    """Create club memberships in admin."""

    model = ClubMembership
    extra = 1


class ClubAdmin(admin.ModelAdmin):
    """Admin config for Clubs."""

    inlines = [ClubMembershipInlineAdmin]
    list_display = ["name", "members_count", "created_at"]

    def members_count(self, obj):
        return obj.memberships.count()


admin.site.register(Club, ClubAdmin)
