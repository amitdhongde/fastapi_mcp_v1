""" Service for Note model. """
from ..repositories import NoteRepository
from ..models import Note

class NoteService:
    def __init__(self):
        self.repository = NoteRepository()

    async def index(self):
        return await self.repository.index()

    async def show(self, hash: str):
        return await self.repository.show(hash)

    async def create(self, note: Note):
        return await self.repository.create(note)

    async def update(self, hash: str, note: Note):
        return await self.repository.update(hash, note)

    async def delete(self, hash: str):
        return await self.repository.delete(hash)
