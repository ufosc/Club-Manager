from typing import Optional
from django.db.models.signals import post_save
from django.dispatch import receiver

from clubs.models import QRCode, RecurringEvent
from clubs.services import ClubService
from lib.qrcodes import create_qrcode_image


@receiver(post_save, sender=RecurringEvent)
def on_save_recurring_event(sender, **kwargs):
    recurring_event = kwargs.get("instance", None)

    if not kwargs.get("created", False):
        return

    ClubService.sync_recurring_event(recurring_event)


@receiver(post_save, sender=QRCode)
def on_save_qrcode(sender, instance: Optional[QRCode], **kwargs):
    if instance.image:
        return

    img_path = create_qrcode_image(instance.url)
    instance.save_image(img_path)
