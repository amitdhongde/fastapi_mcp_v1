""" Import the required modules """
from modules.base.events.base import BaseEvent

class NoteCreatedEvent(BaseEvent):
    """
    Event triggered when a note is created.
    """

    event_name: str = "note_created_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the note created event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)

class NoteUpdatedEvent(BaseEvent):
    """
    Event triggered when a note is updated.
    """

    event_name: str = "note_updated_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the note updated event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)

class NoteDeletedEvent(BaseEvent):
    """
    Event triggered when a note is deleted.
    """

    event_name: str = "note_deleted_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the note deleted event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)