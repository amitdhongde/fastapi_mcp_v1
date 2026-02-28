""" Import the required modules """
from modules.base.events import BaseEvent

class UserCreatedEvent(BaseEvent):
    """
    Event triggered when a user is created.
    """

    event_name: str = "user_created_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the login event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)

class UserUpdatedEvent(BaseEvent):
    """
    Event triggered when a user is updated.
    """

    event_name: str = "user_updated_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the login event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)

class UserDeletedEvent(BaseEvent):
    """
    Event triggered when a user is deleted.
    """

    event_name: str = "user_deleted_event"

    # def __init__(self):
    #     super().__init__()

    # @staticmethod
    # def register(func):
    #     return super().register(func)

    # @staticmethod
    # def raise_event(data: dict):
    #     """
    #     Raises the login event.

    #     Args:
    #         data (dict): The data associated with the event.
    #     """
    #     return super().post_event(data)
