from django.db.models.signals import post_save
from django.dispatch import receiver

from clubs.models import QRCode, RecurringEvent
from lib.qrcodes import create_qrcode_image


@receiver(post_save, sender=RecurringEvent)
def on_save_recurring_event(sender, **kwargs):
    recurring_event = kwargs.get("instance", None)

    if not kwargs.get("created", False):
        return

    recurring_event.sync_events()


@receiver(post_save, sender=QRCode)
def on_save_qrcode(sender, **kwargs):
    obj: QRCode = kwargs.get("instance", None)

    if not kwargs.get("created", False):
        return

    img_path = create_qrcode_image(obj.url)
    obj.image = img_path
    obj.save()
