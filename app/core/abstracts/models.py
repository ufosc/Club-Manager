"""
Abstract models for common fields.
"""

from django.db import models
import uuid


class BaseModel(models.Model):
    """
    Default fields for all models.

    Initializes created_at and updated_at fields,
    default __str__ method that returns name or display_name
    if the field exists on the model.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self) -> str:
        if hasattr(self, "name"):
            return self.name
        elif hasattr(self, "display_name"):
            return self.display_name

        return super().__str__()

    class Meta:
        abstract = True


class UniqueModel(BaseModel):
    """Default fields for globally unique database objects.

    id: Technical id and primary key, never revealed publicly outside of db.
        - If needed to change, it would need to be changed for every
          reference in database, which could cause linking issues

    uuid: Business id, can be shown to public or other services
        - If needed to change, regenerating would be easy and
          the only sideeffect is external services that use id. This could
          be solved by event-based communication between services.
    """

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True
