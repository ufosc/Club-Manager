"""
Club Polls Admin.
"""

from django.contrib import admin

from clubs.polls.models import (
    ChoiceInput,
    ChoiceInputOption,
    Poll,
    PollField,
    PollMarkup,
    PollQuestion,
    PollSubmission,
    RangeInput,
    TextInput,
    UploadInput,
)


class TextInputInlineAdmin(admin.TabularInline):
    """Manage text inputs in questions admin."""

    model = TextInput
    extra = 0


class ChoiceInputInlineAdmin(admin.TabularInline):
    """Manage choice inputs in questions admin."""

    model = ChoiceInput
    extra = 0


class RangeInputInlineAdmin(admin.TabularInline):
    """Manage range inputs in questions admin."""

    model = RangeInput
    extra = 0


class UploadInputInlineAdmin(admin.TabularInline):
    """Manage file upload inputs in questions admin."""

    model = UploadInput
    extra = 0


class PollQuestionAdmin(admin.ModelAdmin):
    """Manage poll questions in admin."""

    inlines = (
        TextInputInlineAdmin,
        ChoiceInputInlineAdmin,
        RangeInputInlineAdmin,
        UploadInputInlineAdmin,
    )


class PollFieldInlineAdmin(admin.StackedInline):
    """Manage fields in poll admin."""

    model = PollField
    extra = 1


class PollAdmin(admin.ModelAdmin):
    """Manage poll objects in admin."""

    inlines = (PollFieldInlineAdmin,)


admin.site.register(Poll, PollAdmin)
admin.site.register(PollQuestion, PollQuestionAdmin)
admin.site.register(PollMarkup)
admin.site.register(ChoiceInputOption)
admin.site.register(PollSubmission)
