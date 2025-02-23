from django.core import exceptions
from clubs.polls.models import (
    Poll,
    PollField,
    PollPageBreak,
    PollQuestion,
    PollInputType,
    TextInput,
)
from core.abstracts.tests import TestsBase
from lib.faker import fake


class PollModelTests(TestsBase):
    """Basic tests for poll models."""

    def test_create_poll(self):
        """Should create a new poll with fields."""

        poll = Poll.objects.create(name=fake.title(), description=fake.paragraph())
        question = PollQuestion.objects.create(
            label="Example question", input_type=PollInputType.TEXT
        )
        PollField.objects.create(poll=poll, question=question, order=0)

        self.assertEqual(TextInput.objects.count(), 1)

    def test_poll_field_union(self):
        """Poll field should only be one of question, markup, or page break."""

        poll = Poll.objects.create(name=fake.title(), description=fake.paragraph())
        question = PollQuestion.objects.create(
            label="Example question", input_type=PollInputType.TEXT
        )
        page_break = PollPageBreak.objects.create()

        with self.assertRaises(exceptions.ValidationError):
            PollField.objects.create(
                poll=poll, question=question, page_break=page_break, order=0
            )
