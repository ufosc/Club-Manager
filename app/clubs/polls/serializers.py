"""
Convert poll models to json objects.
"""

from rest_framework import serializers
from clubs.polls import models
from core.abstracts.serializers import (
    ModelSerializer,
    ModelSerializerBase,
    StringListField,
)


class TextInputNestedSerializer(ModelSerializerBase):
    """Show text input in poll question json."""

    class Meta:
        model = models.TextInput
        fields = ["id", "text_type", "min_length", "max_length"]


class ChoiceInputOptionNestedSerializer(ModelSerializerBase):
    """Show choice input options in poll question json."""

    value = serializers.CharField(required=False)

    class Meta:
        model = models.ChoiceInputOption
        fields = ["id", "label", "value", "image", "order"]


class ChoiceInputNestedSerializer(ModelSerializerBase):
    """Show choice input in poll question json."""

    options = ChoiceInputOptionNestedSerializer(many=True)

    class Meta:
        model = models.ChoiceInput
        fields = ["id", "options"]


class RangeInputNestedSerializer(ModelSerializerBase):
    """Show range input in poll question json."""

    class Meta:
        model = models.RangeInput
        fields = ["id", "min_value", "max_value", "step", "initial_value", "unit"]


class UploadInputNestedSerializer(ModelSerializerBase):
    """Show upload input in poll question json."""

    file_types = StringListField(required=False)

    class Meta:
        model = models.UploadInput
        fields = ["id", "file_types", "max_files"]


class PollQuestionNestedSerializer(ModelSerializerBase):
    """Show questions nested in poll fields."""

    text_input = TextInputNestedSerializer(required=False)
    choice_input = ChoiceInputNestedSerializer(required=False)
    range_input = RangeInputNestedSerializer(required=False)
    upload_input = UploadInputNestedSerializer(required=False)

    created_at = None
    updated_at = None

    class Meta:
        model = models.PollQuestion
        exclude = ["created_at", "updated_at"]

    def create(self, validated_data):
        """Create question with nested inputs."""

        text_input = validated_data.pop("text_input", None)
        choice_input = validated_data.pop("choice_input", None)
        range_input = validated_data.pop("range_input", None)
        upload_input = validated_data.pop("upload_input", None)

        if text_input:
            text_input = models.TextInput.objects.create(**text_input)
            validated_data["text_input"] = text_input

        if choice_input:
            options = choice_input.pop("options")
            choice_input = models.ChoiceInput.objects.create(**choice_input)
            validated_data["choice_input"] = choice_input

            for option in options:
                models.ChoiceInputOption.objects.create(input=choice_input, **option)

        if range_input:
            range_input = models.RangeInput.objects.create(**range_input)
            validated_data["range_input"] = range_input

        if upload_input:
            upload_input = models.UploadInput.objects.create(**upload_input)
            validated_data["upload_input"] = upload_input

        return super().create(validated_data)


class PollMarkupNestedSerializer(ModelSerializerBase):
    """Show markup in poll field json."""

    class Meta:
        model = models.PollMarkup
        fields = ["id", "content"]


class PollPageBreakNestedSerializer(ModelSerializerBase):
    """Show page breaks in poll field json."""

    class Meta:
        model = models.PollPageBreak
        fields = ["id"]


class PollFieldNestedSerializer(ModelSerializerBase):
    """Show poll fields nested in polls."""

    question = PollQuestionNestedSerializer(required=False)
    markup = PollMarkupNestedSerializer(required=False)
    page_break = PollPageBreakNestedSerializer(required=False)

    class Meta:
        model = models.PollField
        fields = ["id", "field_type", "order", "question", "page_break", "markup"]


class PollSerializer(ModelSerializer):
    """JSON definition for polls."""

    fields = PollFieldNestedSerializer(many=True)

    class Meta:
        model = models.Poll
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        """Create poll with nested fields."""

        fields = validated_data.pop("fields")
        poll = super().create(validated_data)

        for field in fields:
            question = field.pop("question", None)
            markup = field.pop("markup", None)
            page_break = field.pop("page_break", None)

            if question:
                serializer = PollQuestionNestedSerializer(data=question)
                serializer.is_valid(raise_exception=True)

                field["question"] = serializer.save()

            if markup:
                serializer = PollMarkupNestedSerializer(data=markup)
                serializer.is_valid(raise_exception=True)

                field["markup"] = serializer.save()

            if page_break:
                serializer = PollPageBreakNestedSerializer(data=page_break)
                serializer.is_valid(raise_exception=True)

                field["page_break"] = serializer.save()

            models.PollField.objects.create(poll=poll, **field)

        return poll
