"""
Custom forms for clubs.
Form interface is a mixture between Google Forms, Jupyter Notebook,
Gravity Forms, and SendGrid.

Google Forms: Mimic form data structure
Jupyter Notebook: Mimic markup capabilities
Gravity Forms: Naming conventions
SendGrid: Versioning (later)

API Inspiration: https://developers.google.com/workspace/forms/api/reference/rest/v1/forms

Structure:
Poll
-- Field
-- -- Question
-- -- Page Break
-- -- Markup
"""

from typing import ClassVar
from django.core import exceptions
from django.db import models
from core.abstracts.models import ManagerBase, ModelBase
from users.models import User


class PollInputType(models.TextChoices):
    """Types of fields a user can add to a poll."""

    SHORT_TEXT = "short_text"
    LONG_TEXT = "long_text"
    CHOICE = "choice"
    RANGE = "range"
    UPLOAD = "upload"


class PollFieldType(models.TextChoices):
    """Different types of fields that can be added to a poll."""

    QUESTION = "question"
    PAGE_BREAK = "page_break"
    MARKUP = "markup"


class PollManager(ManagerBase["Poll"]):
    """Manage queries for polls."""

    def create(self, name: str, **kwargs):
        return super().create(name=name, **kwargs)


class Poll(ModelBase):
    """Custom form."""

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    # Overrides
    objects: ClassVar[PollManager] = PollManager()


class ShortTextInput(ModelBase):
    """Single line input."""

    value = models.CharField(max_length=255, default="")


class LongTextInput(ModelBase):
    """Textarea input."""

    value = models.TextField(default="")


class ChoiceInput(ModelBase):
    """Dropdown or radio field."""

    multiple = models.BooleanField(default=False)


class ChoiceInputOption(ModelBase):
    """Option element inside select field."""

    input = models.ForeignKey(
        ChoiceInput, on_delete=models.CASCADE, related_name="options"
    )

    label = models.CharField(default="")
    value = models.CharField(default="")


class RangeInput(ModelBase):
    """Slider input."""

    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=100)
    initial_value = models.IntegerField(default=0)


class UploadInput(ModelBase):
    """Upload button, file input."""

    pass


class PollQuestionManager(ManagerBase["PollQuestion"]):
    """Manage queries for Poll Questions."""

    def create(
        self,
        label: str,
        question_type: PollInputType,
        question_kwargs=None,
        **kwargs,
    ):
        input_class = None
        question_kwargs = question_kwargs or {}

        match question_type:
            case PollInputType.SHORT_TEXT:
                input_class = ShortTextInput
                input_name = "short_text_input"
            case PollInputType.LONG_TEXT:
                input_class = LongTextInput
                input_name = "long_text_input"
            case PollInputType.CHOICE:
                input_class = ChoiceInput
                input_name = "choice_input"
            case PollInputType.RANGE:
                input_class = RangeInput
                input_name = "range_input"
            case PollInputType.UPLOAD:
                input_class = UploadInput
                input_name = "upload_input"
            case _:
                input_class = ShortTextInput
                input_name = "short_text_input"

        input = input_class.objects.create(**question_kwargs)

        return super().create(
            label=label, question_type=question_type, **{input_name: input}, **kwargs
        )


class PollQuestion(ModelBase):
    """
    Record user input.

    Whether a field is required is determined at question (this) level,
    all fields will have defaults.

    Validation is handled at the field level.
    """

    label = models.TextField()
    question_type = models.CharField(
        choices=PollInputType.choices, default=PollInputType.SHORT_TEXT
    )
    required = models.BooleanField(default=False)

    # Union - Only one of these
    short_text_input = models.OneToOneField(
        ShortTextInput,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )
    long_text_input = models.OneToOneField(
        LongTextInput,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )
    choice_input = models.OneToOneField(
        ChoiceInput,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )
    range_input = models.OneToOneField(
        RangeInput,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )
    upload_input = models.OneToOneField(
        UploadInput,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="question",
    )

    # Overrides
    objects: ClassVar[PollQuestionManager] = PollQuestionManager()

    class Meta:
        # Implement validation at db level to ensure integrety
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(
                        short_text_input__isnull=False,
                        long_text_input__isnull=True,
                        choice_input__isnull=True,
                        range_input__isnull=True,
                        upload_input__isnull=True,
                    )
                    | models.Q(
                        short_text_input__isnull=True,
                        long_text_input__isnull=False,
                        choice_input__isnull=True,
                        range_input__isnull=True,
                        upload_input__isnull=True,
                    )
                    | models.Q(
                        short_text_input__isnull=True,
                        long_text_input__isnull=True,
                        choice_input__isnull=False,
                        range_input__isnull=True,
                        upload_input__isnull=True,
                    )
                    | models.Q(
                        short_text_input__isnull=True,
                        long_text_input__isnull=True,
                        choice_input__isnull=True,
                        range_input__isnull=False,
                        upload_input__isnull=True,
                    )
                    | models.Q(
                        short_text_input__isnull=True,
                        long_text_input__isnull=True,
                        choice_input__isnull=True,
                        range_input__isnull=True,
                        upload_input__isnull=False,
                    )
                ),
                name="poll_question_union_type",
            )
        ]

    def clean(self):
        """Validate data before it get's to db, offer detailed errors."""
        nonnull_fields = [
            field
            for field in [
                self.short_text_input,
                self.long_text_input,
                self.choice_input,
                self.range_input,
                self.upload_input,
            ]
            if field is not None
        ]

        if len(nonnull_fields) > 1:
            raise exceptions.ValidationError(
                f'Cannot set fields {", ".join(nonnull_fields)} at the same time.'
            )

        return super().clean()


class PollPageBreak(ModelBase):
    """Indicates poll continues on next page."""

    pass


class PollMarkup(ModelBase):
    """Store markdown content for a poll."""

    content = models.TextField(default="")


class PollField(ModelBase):
    """Custom question field for poll forms."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="items")
    field_type = models.CharField(choices=PollFieldType.choices)

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

    # Overrides
    class Meta:
        constraints = [
            models.CheckConstraint(
                name="poll_field_union_type",
                condition=(
                    models.Q(
                        field_type=PollFieldType.QUESTION,
                        question__isnull=False,
                        page_break__isnull=True,
                        markup__isnull=True,
                    )
                    | models.Q(
                        field_type=PollFieldType.PAGE_BREAK,
                        question__isnull=True,
                        page_break__isnull=False,
                        markup__isnull=True,
                    )
                    | models.Q(
                        field_type=PollFieldType.MARKUP,
                        question__isnull=True,
                        page_break__isnull=True,
                        markup__isnull=False,
                    )
                ),
            )
        ]

    def clean(self):
        nonnull_fields = [
            field
            for field in [self.question, self.page_break, self.markup]
            if field is not None
        ]

        if len(nonnull_fields) > 1:
            raise exceptions.ValidationError(
                f'Cannot set fields {", ".join(nonnull_fields)} at the same time.'
            )

        return super().clean()

    def save(self, *args, **kwargs):
        if self.field_type is None:
            if self.question is not None:
                self.field_type = PollFieldType.QUESTION
            elif self.page_break is not None:
                self.field_type = PollFieldType.PAGE_BREAK
            elif self.markup is not None:
                self.field_type = PollFieldType.MARKUP

        return super().save(*args, **kwargs)


class PollSubmission(ModelBase):
    """Records a person's input for a poll."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="poll_submissions",
        null=True,
        blank=True,
    )
    data = models.JSONField(null=True, blank=True)
