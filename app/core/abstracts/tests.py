from typing import Optional, Type
from django import forms
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from users.tests.utils import create_test_adminuser


class TestsBase(TestCase):
    """Abstract testing utilities."""

    def assertObjFields(self, object, fields: dict):
        """Object fields should match given field values."""
        for key, value in fields.items():
            obj_value = getattr(object, key)
            self.assertEqual(obj_value, value)

    def assertNotImplemented(self):
        """Mark a test as not implemented, should fail."""
        self.fail("Method is not implemented.")

    def assertLength(self, target: list, length=1, msg=None):
        """Provided list should be specified length."""
        if msg is None:
            msg = f"Invalid length of {len(target)}, expected {length}."

        self.assertEqual(len(target), length, msg)


class ApiTestsBase(TestsBase):
    """Abstract testing utilities for api testing."""

    def setUp(self):
        self.client = APIClient()

    def assertOk(self, reverse_url: str, reverse_kwargs=None):
        reverse_kwargs = reverse_kwargs if reverse_kwargs else {}
        url = reverse(reverse_url, **reverse_kwargs)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class ViewsTestsBase(ApiTestsBase):
    """Abstract testing utilities for app views."""

    def assertRenders(
        self,
        url: Optional[str] = None,
        reverse_url: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """Reversible url should return 200."""
        path = (
            reverse(reverse_url, args=[*args], kwargs={**kwargs})
            if reverse_url
            else url
        )
        assert path is not None

        res = self.client.get(path)
        self.assertEqual(res.status_code, HTTP_200_OK)

        return res

    def assertHasForm(
        self,
        res: HttpResponse,
        form_class: Type[forms.Form],
        initial_data: dict | None = None,
    ) -> forms.Form:
        """Response should have a form object."""

        form: forms.Form | None = res.context.get("form", None)
        self.assertIsInstance(form, form_class)
        assert form is not None

        if initial_data:
            for key, value in initial_data.items():
                if value:
                    self.assertIn(key, form.initial.keys())

                self.assertEqual(form.initial.get(key, None), value)

        return form


class AuthViewsTestsBase(ViewsTestsBase):
    """Abstract testing utilities for app views that require auth."""

    def setUp(self):
        super().setUp()
        self.user = create_test_adminuser()

        self.client = APIClient()
        self.client.force_login(user=self.user)
