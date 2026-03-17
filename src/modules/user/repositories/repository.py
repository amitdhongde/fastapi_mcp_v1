""" Import the required modules """
from modules.base.repository import BaseRepository

# Import the schema and model classes
from modules.user.schemas import UserSchema

class UserRepository(BaseRepository[UserSchema]):
    """
    This class to handle object related database operations.

    This class provides methods to perform CRUD operations on the database.
    It uses SQLAlchemy to interact with the database.
    """
    def __init__(self, model = UserSchema):
        self.model = model
        super().__init__(model)
