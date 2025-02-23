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
-- -- Question
-- -- Page Break
-- -- Markup
"""

from typing import ClassVar, Optional
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


class TextInput(ModelBase):
    """
    Text input, textarea, or rich text editor.

    If character count is 0, then field is empty, and should
    raise error if the field is required.
    """

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
    value = models.CharField(blank=True, default="", max_length=100)
    image = models.ImageField(null=True, blank=True)
    order = models.IntegerField()

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

    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=100)
    step = models.IntegerField(default=1)
    initial_value = models.IntegerField(default=0)
    unit = models.CharField(max_length=10, null=True, blank=True)


class UploadInput(ModelBase):
    """Upload button, file input."""

    # TODO: How to handle list of file types?
    file_types = models.CharField(default="any")
    max_files = models.IntegerField(default=1)


class PollQuestionManager(ManagerBase["PollQuestion"]):
    """Manage queries for Poll Questions."""

    def create(
        self,
        label: str,
        input_type: PollInputType,
        question_kwargs=None,
        **kwargs,
    ):
        input_class = None
        input_name = None
        question_kwargs = question_kwargs or {}

        match input_type:
            case PollInputType.TEXT:
                if kwargs.get("text_input") is None:
                    input_class = TextInput
                    input_name = "text_input"
            case PollInputType.CHOICE:
                if kwargs.get("choice_input") is None:
                    input_class = ChoiceInput
                    input_name = "choice_input"
            case PollInputType.RANGE:
                if kwargs.get("range_input") is None:
                    input_class = RangeInput
                    input_name = "range_input"
            case PollInputType.UPLOAD:
                if kwargs.get("upload_input") is None:
                    input_class = UploadInput
                    input_name = "upload_input"
            case _:
                if kwargs.get("text_input") is None:
                    input_class = TextInput
                    input_name = "text_input"

        if input_class is not None:
            input = input_class.objects.create(**question_kwargs)
            kwargs[input_name] = input

        return super().create(label=label, input_type=input_type, **kwargs)


class PollQuestion(ModelBase):
    """
    Record user input.

    Whether a field is required is determined at question (this) level,
    all fields will have defaults.

    Validation is handled at the field level.
    """

    label = models.CharField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    required = models.BooleanField(default=False)

    input_type = models.CharField(
        choices=PollInputType.choices, default=PollInputType.TEXT
    )

    # Union - Only one of these
    text_input = models.OneToOneField(
        TextInput,
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
                check=(
                    models.Q(
                        text_input__isnull=False,
                        choice_input__isnull=True,
                        range_input__isnull=True,
                        upload_input__isnull=True,
                    )
                    | models.Q(
                        text_input__isnull=True,
                        choice_input__isnull=False,
                        range_input__isnull=True,
                        upload_input__isnull=True,
                    )
                    | models.Q(
                        text_input__isnull=True,
                        choice_input__isnull=True,
                        range_input__isnull=False,
                        upload_input__isnull=True,
                    )
                    | models.Q(
                        text_input__isnull=True,
                        choice_input__isnull=True,
                        range_input__isnull=True,
                        upload_input__isnull=False,
                    )
                    | models.Q(
                        text_input__isnull=True,
                        choice_input__isnull=True,
                        range_input__isnull=True,
                        upload_input__isnull=True,
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
                self.text_input,
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


class PollFieldManager(ManagerBase["PollField"]):
    """Manage queries for Poll Fields."""

    def create(
        self,
        poll: Poll,
        order: int,
        field_type: Optional[PollFieldType] = None,
        question=None,
        page_break=None,
        markup=None,
        **kwargs,
    ):

        if field_type == PollFieldType.PAGE_BREAK:
            if page_break is None:
                page_break = PollPageBreak.objects.create()
        elif field_type == PollFieldType.MARKUP:
            if markup is None:
                markup = PollMarkup.objects.create()

        return super().create(
            poll=poll,
            field_type=field_type,
            order=order,
            question=question,
            page_break=page_break,
            markup=markup,
            **kwargs,
        )


class PollField(ModelBase):
    """Custom question field for poll forms."""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="fields")
    field_type = models.CharField(
        choices=PollFieldType.choices, default=PollFieldType.QUESTION
    )
    order = models.IntegerField()

    # Union - Can only be one of the following
    question = models.OneToOneField(
        PollQuestion,
        on_delete=models.SET_NULL,
        related_name="field",
        null=True,
        blank=True,
    )
    page_break = models.OneToOneField(
        PollPageBreak,
        on_delete=models.SET_NULL,
        related_name="field",
        null=True,
        blank=True,
    )
    markup = models.OneToOneField(
        PollMarkup,
        on_delete=models.SET_NULL,
        related_name="field",
        null=True,
        blank=True,
    )

    # Overrides
    objects: ClassVar[PollFieldManager] = PollFieldManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_field_order_per_poll", fields=("order", "poll")
            ),
            models.CheckConstraint(
                name="poll_field_union_type",
                check=(
                    models.Q(
                        field_type=PollFieldType.QUESTION,
                        page_break__isnull=True,
                        markup__isnull=True,
                    )
                    | models.Q(
                        field_type=PollFieldType.PAGE_BREAK,
                        question__isnull=True,
                        markup__isnull=True,
                    )
                    | models.Q(
                        field_type=PollFieldType.MARKUP,
                        question__isnull=True,
                        page_break__isnull=True,
                    )
                    | models.Q(
                        question__isnull=True,
                        page_break__isnull=True,
                        markup__isnull=True,
                    )
                ),
            ),
        ]

    def clean(self):
        """
        Validate data before it hits database.
        Sends Validation Error before database sends Integrety Error,
        has better UX.
        """
        # Check union fields
        nonnull_fields = [
            field[1]
            for field in [
                (self.question, "question"),
                (self.page_break, "page break"),
                (self.markup, "markup"),
            ]
            if field[0] is not None
        ]

        if len(nonnull_fields) > 1:
            raise exceptions.ValidationError(
                f'Cannot set fields {", ".join(nonnull_fields)} at the same time.'
            )

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
