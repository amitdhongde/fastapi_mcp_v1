""" Import the required modules """
from modules.base.events.base import BaseEvent

class DocumentCreatedEvent(BaseEvent):
    """
    Event triggered when a document is created.
    """

    event_name: str = "document_created_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the document created event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)

class DocumentUpdatedEvent(BaseEvent):
    """
    Event triggered when a document is updated.
    """

    event_name: str = "document_updated_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the document updated event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)

class DocumentDeletedEvent(BaseEvent):
    """
    Event triggered when a document is deleted.
    """

    event_name: str = "document_deleted_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the document deleted event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)