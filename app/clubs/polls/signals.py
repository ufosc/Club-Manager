from django.db.models.signals import post_save
from django.dispatch import receiver

from clubs.polls.models import (
    ChoiceInput,
    PollInputType,
    PollQuestion,
    RangeInput,
    TextInput,
    UploadInput,
)


@receiver(post_save, sender=PollQuestion)
def on_save_pollquestion(sender, instance: PollQuestion, created=False, **kwargs):
    """Automations to run when field is saved."""

    if instance.input_type == PollInputType.TEXT and instance.text_input is None:
        TextInput.objects.create(question=instance)
    elif instance.input_type == PollInputType.CHOICE and instance.choice_input is None:
        ChoiceInput.objects.create(question=instance)
    elif instance.input_type == PollInputType.RANGE and instance.range_input is None:
        RangeInput.objects.create(question=instance)
    elif instance.input_type == PollInputType.UPLOAD and instance.upload_input is None:
        UploadInput.objects.create(question=instance)
