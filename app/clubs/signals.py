from django.db.models.signals import post_save
from django.dispatch import receiver

from clubs.models import RecurringEvent


@receiver(post_save, sender=RecurringEvent)
def on_save_recurring_event(sender, **kwargs):
    recurring_event = kwargs.get("instance", None)

    if not kwargs.get("created", False):
        return

    recurring_event.sync_events()
