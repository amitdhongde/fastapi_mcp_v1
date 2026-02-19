""" Repository for Note model. """
from ..models import Note

class NoteRepository():
    def __init__(self):
        #super().__init__(Note)
        pass

    async def index(self):
        return 'NoteRepository index'

    async def show(self, hash: str):
        return f'NoteRepository show {hash}'

    async def create(self, note: Note):
        return 'NoteRepository create'

    async def update(self, hash: str, note: Note):
        return f'NoteRepository update {hash}'

    async def delete(self, hash: str):
        return f'NoteRepository delete {hash}'
