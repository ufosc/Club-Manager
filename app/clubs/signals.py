from django.db.models.signals import post_save
from django.dispatch import receiver

from clubs.models import RecurringEvent
from clubs.services import ClubService


@receiver(post_save, sender=RecurringEvent)
def on_save_recurring_event(sender, **kwargs):
    recurring_event = kwargs.get("instance", None)

    if not kwargs.get("created", False):
        return

    ClubService.sync_recurring_event(recurring_event)
