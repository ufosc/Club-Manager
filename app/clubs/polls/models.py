"""
Custom forms for clubs.
Form interface is a mixture between Google Forms, Jupyter Notebook,
Gravity Forms (WordPress plugin), and SendGrid.

Google Forms: Mimic form data structure
Jupyter Notebook: Mimic markup capabilities
Gravity Forms: Naming conventions
SendGrid: Versioning (later)

API Inspiration: https://developers.google.com/workspace/forms/api/reference/rest/v1/forms

Structure:
Poll
-- Field
-- -- Page Break
-- -- Markup
-- -- Question
-- -- -- Text Input (short, long, rich)
-- -- -- Choice Input (single, multiple)
-- -- -- Range Input
-- -- -- Upload Input
"""

from typing import ClassVar
from django.core import exceptions
from django.core.validators import MinValueValidator
from django.db import models
from core.abstracts.models import ManagerBase, ModelBase
from users.models import User


class PollInputType(models.TextChoices):
    """Types of fields a user can add to a poll."""

    TEXT = "text"
    CHOICE = "choice"
    RANGE = "range"
    UPLOAD = "upload"


class PollFieldType(models.TextChoices):
    """Different types of fields that can be added to a poll."""

    QUESTION = "question"
    PAGE_BREAK = "page_break"
    MARKUP = "markup"


class PollTextInputType(models.TextChoices):
    """Different ways of inputing text responses."""

    SHORT = "short"
    LONG = "long"
    RICH = "rich"


class PollSingleChoiceType(models.TextChoices):
    """Different ways of showing single choice fields."""

    SELECT = "select"
    RADIO = "radio"


class PollMultiChoiceType(models.TextChoices):
    """Different ways of showing multichoice fields."""

    SELECT = "select"
    CHECKBOX = "checkbox"


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


class PollField(ModelBase):
    """Custom question field for poll forms."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="fields")
    field_type = models.CharField(
        choices=PollFieldType.choices, default=PollFieldType.QUESTION
    )
    order = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_field_order_per_poll", fields=("order", "poll")
            ),
        ]

    def clean(self):
        """
        Validate data before it hits database.
        Sends Validation Error before database sends Integrety Error,
        has better UX.
        """

        # Check order field
        order_query = PollField.objects.filter(poll=self.poll, order=self.order)
        if order_query.count() > 1:
            raise exceptions.ValidationError(
                f"Multiple fields are set to order {self.order}."
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


class PollMarkup(ModelBase):
    """Store markdown content for a poll."""

    field = models.OneToOneField(
        PollField, on_delete=models.CASCADE, related_name="markup"
    )
    content = models.TextField(default="")


class PollQuestionManager(ManagerBase["PollQuestion"]):
    """Manage question queries."""

    def create(
        self,
        field: PollField,
        label: str,
        input_type: PollInputType,
        create_input=False,
        **kwargs,
    ):

        question = super().create(
            field=field, label=label, input_type=input_type, **kwargs
        )

        if not create_input:
            return question

        match input_type:
            case PollInputType.TEXT:
                TextInput.objects.create(question=question)
            case PollInputType.CHOICE:
                ChoiceInput.objects.create(question=question)
            case PollInputType.RANGE:
                RangeInput.objects.create(question=question)
            case PollInputType.UPLOAD:
                UploadInput.objects.create(question=question)

        return question


class PollQuestion(ModelBase):
    """
    Record user input.

    Whether a field is required is determined at question (this) level,
    all fields will have defaults.

    Validation is handled at the field level.
    """

    field = models.OneToOneField(
        PollField, on_delete=models.CASCADE, related_name="question"
    )

    input_type = models.CharField(
        choices=PollInputType.choices, default=PollInputType.TEXT
    )
    label = models.CharField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    required = models.BooleanField(default=False)

    # Overrides
    objects: ClassVar[PollQuestionManager] = PollQuestionManager()


class TextInput(ModelBase):
    """
    Text input, textarea, or rich text editor.

    If character count is 0, then field is empty, and should
    raise error if the field is required.
    """

    question = models.OneToOneField(
        PollQuestion, on_delete=models.CASCADE, related_name="text_input"
    )

    text_type = models.CharField(
        choices=PollTextInputType.choices, default=PollTextInputType.SHORT
    )
    min_length = models.PositiveIntegerField(
        null=True, blank=True, default=1, validators=[MinValueValidator(1)]
    )
    max_length = models.PositiveIntegerField(null=True, blank=True)

    # Overrides
    class Meta:
        constraints = [
            models.CheckConstraint(
                name="min_length_less_than_max_length",
                check=models.Q(min_length__lt=models.F("max_length")),
            ),
        ]


class ChoiceInput(ModelBase):
    """Dropdown or radio field."""

    question = models.OneToOneField(
        PollQuestion, on_delete=models.CASCADE, related_name="choice_input"
    )

    multiple = models.BooleanField(default=False)
    multiple_choice_type = models.CharField(
        choices=PollMultiChoiceType.choices,
        null=True,
        blank=True,
        default=PollMultiChoiceType.CHECKBOX,
    )
    single_choice_type = models.CharField(
        choices=PollSingleChoiceType.choices,
        null=True,
        blank=True,
        default=PollSingleChoiceType.RADIO,
    )

    # Overrides
    class Meta:
        constraints = [
            # Multiple/single choice types can be set at same time,
            # so if user toggles between them their preference is saved.
            models.CheckConstraint(
                name="poll_choice_type",
                check=(
                    models.Q(multiple=True, multiple_choice_type__isnull=False)
                    | models.Q(multiple=False, single_choice_type__isnull=False)
                ),
            )
        ]

    def save(self, *args, **kwargs):
        # Enforce defaults, in case user deletes field type but keeps "multiple" selection
        if self.multiple is True and self.multiple_choice_type is None:
            self.multiple_choice_type = PollMultiChoiceType.CHECKBOX
        elif self.multiple is False and self.single_choice_type is None:
            self.single_choice_type = PollSingleChoiceType.RADIO

        return super().save(*args, **kwargs)


class ChoiceInputOption(ModelBase):
    """Option element inside select field."""

    input = models.ForeignKey(
        ChoiceInput, on_delete=models.CASCADE, related_name="options"
    )

    label = models.CharField(max_length=100)
    order = models.IntegerField()
    value = models.CharField(blank=True, default="", max_length=100)
    image = models.ImageField(null=True, blank=True)

    # Overrides
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_choiceoption_order_per_input", fields=("order", "input")
            ),
        ]

    def clean(self):
        """Validate data before it hits database."""

        # Allow user to only provide label, value will sync
        if self.value is None or self.value.strip() == "":
            self.value = self.label

        return super().clean()


class RangeInput(ModelBase):
    """Slider input."""

    question = models.OneToOneField(
        PollQuestion, on_delete=models.CASCADE, related_name="range_input"
    )

    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=100)
    step = models.IntegerField(default=1)
    initial_value = models.IntegerField(default=0)
    unit = models.CharField(max_length=10, null=True, blank=True)


class UploadInput(ModelBase):
    """Upload button, file input."""

    question = models.OneToOneField(
        PollQuestion, on_delete=models.CASCADE, related_name="upload_input"
    )

    # TODO: How to handle list of file types?
    file_types = models.CharField(default="any")
    max_files = models.IntegerField(default=1)


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
