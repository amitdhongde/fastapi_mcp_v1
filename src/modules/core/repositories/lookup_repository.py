""" Import the required modules """
from modules.base.repository import BaseRepository

# Import the schema and model classes
from modules.core.schemas import LookupSchema

class LookupRepository(BaseRepository[LookupSchema]):
    """
    This class to handle object related database operations.
    
    This class provides methods to perform CRUD operations on the database.
    It uses SQLAlchemy to interact with the database.
    """
    def __init__(self, model = LookupSchema):
        self.model = model
        super().__init__(model)
