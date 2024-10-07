from core.abstracts.services import ModelService


CLUB_CREATE_PARAMS = {
    "name": "Test Club",
}
CLUB_UPDATE_PARAMS = {"name": "Updated Club"}


class ModelServiceTestsMixin(object):
    """Base tests for model services."""

    # service = ClubService
    # create_params = CLUB_CREATE_PARAMS
    # update_params = CLUB_UPDATE_PARAMS

    service = ModelService
    create_params = {}
    update_params = {}

    def setUp(self) -> None:
        self.model = self.service.model

        return super().setUp()

    def test_create_model(self):
        """Service should create model."""

        obj = self.service.create(**self.create_params)
        self.assertObjFields(obj, self.create_params)

    def test_find_by_id(self):
        """Service should find model by id."""
        self.assertNotImplemented()

    def test_find_one(self):
        """Service should find one model."""
        self.assertNotImplemented()

    def test_find(self):
        """Service should find models with params."""
        self.assertNotImplemented()

    def test_update_one(self):
        """Service should find and update one model."""
        self.assertNotImplemented()

    def test_update_models(self):
        """Service should update model."""
        self.assertNotImplemented()

    def test_delete_one(self):
        """Service should find one model and delete."""
        self.assertNotImplemented()

    def test_delete_models(self):
        """Service should delete models that match params."""
        self.assertNotImplemented()
