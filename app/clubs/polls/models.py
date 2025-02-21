"""
Custom forms for clubs.
Form interface is a mixture between Google Forms, Jupyter Notebook, and SendGrid.

Google Forms: Mimic form data
Jupyter Notebook: Mimic markup capabilities
SendGrid: Versioning (later)

API Inspiration: https://developers.google.com/workspace/forms/api/reference/rest/v1/forms

Structure:
Poll
-- Item
-- -- Question
-- -- Page Break
-- -- Markup
"""

from django.db import models
from core.abstracts.models import ModelBase


class PollQuestionType(models.TextChoices):
    """Types of fields a user can add to a poll."""

    SHORT_TEXT = "short_text"
    LONG_TEXT = "long_text"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    RANGE = "range"
    UPLOAD = "upload"


class Poll(ModelBase):
    """Custom form."""

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)


class ShortTextField(ModelBase):
    """Single line input."""

    value = models.CharField(max_length=255, default="")


class LongTextField(ModelBase):
    """Textarea input."""

    value = models.TextField(default="")


class ChoiceField(ModelBase):
    """Dropdown or radio field."""

    pass


class ChoiceFieldOption(ModelBase):
    """Option element inside select field."""

    field = models.ForeignKey(
        ChoiceField, on_delete=models.CASCADE, related_name="options"
    )

    label = models.CharField(default="")
    value = models.CharField(default="")


class RangeField(ModelBase):
    """Slider input."""

    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=100)
    initial_value = models.IntegerField(default=0)


class UploadField(ModelBase):
    """Upload button, file input."""

    pass


class PollQuestion(ModelBase):
    """
    Record user input.

    Whether a field is required is determined at question (this) level,
    all fields will have defaults.

    Validation is handled at the field level.
    """

    text = models.TextField()
    question_type = models.CharField(
        choices=PollQuestionType.choices, default=PollQuestionType.SHORT_TEXT
    )
    required = models.BooleanField(default=False)

    # Union - Only one of these
    short_text_field = models.OneToOneField(
        ShortTextField,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )
    long_text_field = models.OneToOneField(
        LongTextField,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )
    single_choice_field = models.OneToOneField(
        ChoiceField,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="single_question",
    )
    multi_choice_field = models.OneToOneField(
        ChoiceField,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="multi_question",
    )
    range_field = models.OneToOneField(
        RangeField,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )
    upload_field = models.OneToOneField(
        UploadField,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )


class PollPageBreak(ModelBase):
    """Indicates poll continues on next page."""

    pass


class PollMarkup(ModelBase):
    """Store markdown content for a poll."""

    content = models.TextField(default="")


class PollItem(ModelBase):
    """Custom question field for poll forms."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="items")

    # Union - Can only be one of the following
    question = models.OneToOneField(
        PollQuestion,
        on_delete=models.SET_NULL,
        related_name="item",
        null=True,
        blank=True,
    )
    page_break = models.OneToOneField(
        PollPageBreak,
        on_delete=models.SET_NULL,
        related_name="item",
        null=True,
        blank=True,
    )
    markup = models.OneToOneField(
        PollMarkup,
        on_delete=models.SET_NULL,
        related_name="item",
        null=True,
        blank=True,
    )
