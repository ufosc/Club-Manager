"""
Unit tests for generic model functions, validation, etc.
"""

from clubs.models import Club
from clubs.tests.utils import CLUB_CREATE_PARAMS, CLUB_UPDATE_PARAMS
from core.abstracts.tests import TestsBase


class BaseModelTests(TestsBase):
    """Base tests for django models."""

    model = Club
    create_params = CLUB_CREATE_PARAMS
    update_params = CLUB_UPDATE_PARAMS

    def test_create_model(self):
        """Should create model."""
        obj = self.model.objects.create(**self.create_params)
        self.assertIsNotNone(obj.created_at)

        for key, expected_value in self.create_params.items():
            actual_value = getattr(obj, key)

            self.assertEqual(actual_value, expected_value)

    def test_update_model(self):
        """Should update model."""

        obj = self.model.objects.create(**self.create_params)

        for key, expected_value in self.update_params.items():
            actual_value = getattr(obj, key)
            self.assertNotEqual(actual_value, expected_value)

            setattr(obj, key, expected_value)
            obj.save()

            actual_value = getattr(obj, key)
            self.assertEqual(actual_value, expected_value)

    def test_delete_model(self):
        """Should delete model."""

        obj = self.model.objects.create(**self.create_params)

        obj_count = self.model.objects.all().count()
        self.assertEqual(obj_count, 1)

        self.model.objects.filter(id=obj.id).delete()

        obj_count = self.model.objects.all().count()
        self.assertEqual(obj_count, 0)
