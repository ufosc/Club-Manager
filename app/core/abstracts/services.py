from core.abstracts.models import BaseModel
from utils.models import get_or_none


class ModelService:
    """Base service for a model."""

    model = BaseModel

    @classmethod
    def create(cls, *args, **kwargs):
        """Create model."""
        return cls.model.objects.create(*args, **kwargs)

    @classmethod
    def findById(cls, id: int):
        """Find model by its id."""
        return get_or_none(cls.model, id=id)

    @classmethod
    def findOne(cls, **kwargs):
        """Find model using set of fields."""
        return get_or_none(cls.model, **kwargs)

    @classmethod
    def find(cls, **kwargs):
        """Find a list of models matching fields."""
        return cls.model.objects.filter(**kwargs)

    @classmethod
    def updateOne(cls, id: int, **kwargs):
        """Update model by id."""
        return cls.model.objects.filter(id=id).update(**kwargs)

    @classmethod
    def update(cls, query: dict, **kwargs):
        """Update all models matching query."""
        return cls.model.objects.filter(**query).update(**kwargs)

    @classmethod
    def deleteOne(cls, id: int):
        """Delete model with id."""
        return cls.model.objects.filter(id=id).delete()

    @classmethod
    def delete(cls, **kwargs):
        """Delete all models matching fields."""
        return cls.model.objects.filter(**kwargs).delete()
