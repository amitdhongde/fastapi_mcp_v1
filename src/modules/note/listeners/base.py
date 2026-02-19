""" Event handlers for logging note events """
from ..events import NoteCreatedEvent, NoteUpdatedEvent, NoteDeletedEvent

def handle_note_created_event(note):
    print(f"Note created with title: {note.title}")

def handle_note_updated_event(note):
    print(f"Note updated with title: {note.title}")

def handle_note_deleted_event(note):
    print(f"Note deleted with title: {note.title}")

def setup_log_event_handlers():
    NoteCreatedEvent().register(handle_note_created_event)
    NoteUpdatedEvent().register(handle_note_updated_event)
    NoteDeletedEvent().register(handle_note_deleted_event)
    # subscribe("user_registered", handle_user_registered_event)
    # subscribe("user_password_forgotten", handle_user_password_forgotten_event)
    # subscribe("user_upgrade_plan", handle_user_upgrade_plan_event)
