from django.db.models.signals import post_save
from django.dispatch import receiver

from clubs.consts import INITIAL_CLUB_ROLES
from clubs.models import Club, ClubRole, Event, EventAttendanceLink, RecurringEvent
from clubs.services import ClubService


@receiver(post_save, sender=RecurringEvent)
def on_save_recurring_event(sender, instance: RecurringEvent, created=False, **kwargs):
    """Automations to run when a recurring event is saved."""

    if not created:
        # Only proceed if model is being saved for first time
        return

    ClubService.sync_recurring_event(instance)


@receiver(post_save, sender=Event)
def on_save_event(sender, instance: Event, created=False, **kwargs):
    """Automations to run when event is saved."""

    if not created:
        # Only proceed if event is being created
        return

    link = EventAttendanceLink.objects.create(event=instance, reference="Default")
    link.generate_qrcode()


@receiver(post_save, sender=Club)
def on_save_club(sender, instance: Club, created=False, **kwargs):
    """Automations to run when a club is created."""

    if not created:
        # Only proceed if club is being created
        return

    # Create roles after club creation
    for role in INITIAL_CLUB_ROLES:
        ClubRole.objects.create(
            club=instance,
            name=role["name"],
            default=role["default"],
            perm_labels=role["permissions"],
        )
