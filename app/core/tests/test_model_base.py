"""
Unit tests for core base models.
"""

from core.abstracts.tests import TestsBase
from core.mock.models import Buster
from lib.faker import fake


class BaseModelTests(TestsBase):
    """Base model unit tests."""

    def setUp(self):
        self.model_class = Buster

        return super().setUp()

    def test_create_model(self):
        """Should create model."""

        self.assertEqual(self.model_class.objects.count(), 0)
        self.model_class.objects.create(name=fake.sentence(3))
        self.assertEqual(self.model_class.objects.count(), 1)

    def test_find_one(self):
        """Should find one object, or return None"""

        name = fake.sentence(3)
        self.model_class.objects.create(name=name)
        self.model_class.objects.create(name=name)

        self.assertIsInstance(self.model_class.objects.find_one(name=name), self.model_class)

        not_name = fake.sentence(2)
        self.assertIsNone(self.model_class.objects.find_one(name=not_name))

    def test_find_by_id(self):
        """Should find one by id, or return None."""

        name = fake.sentence(3)
        obj1 = self.model_class.objects.create(name=name)
        self.model_class.objects.create(name=name)

        self.assertIsInstance(self.model_class.objects.find_by_id(id=obj1.id), self.model_class)
        self.assertIsNone(self.model_class.objects.find_by_id(id=-1))

    def test_find(self):
        """Should find objects matching query, or return none."""

        name = fake.sentence(3)
        obj1 = self.model_class.objects.create(name=name)
        self.model_class.objects.create(name=name)

        self.assertEqual(self.model_class.objects.find(name=name).count(), 2)
        self.assertEqual(self.model_class.objects.find(id=obj1.id).count(), 1)

        not_name = fake.sentence(2)
        self.assertIsNone(self.model_class.objects.find(name=not_name))

    def test_filter_one(self):
        """Should return first item from filter, or none."""

        name = fake.sentence(3)
        self.model_class.objects.create(name=name)
        self.model_class.objects.create(name=name)

        self.assertIsInstance(self.model_class.objects.find_one(name=name), self.model_class)

        not_name = fake.sentence(2)
        self.assertIsNone(self.model_class.objects.find_one(name=not_name))
