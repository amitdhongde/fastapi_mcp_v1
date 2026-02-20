""" Service for Note model. """
from ..repositories import NoteRepository
from ..models import Note

class NoteService:
    def __init__(self):
        self.repository = NoteRepository()

    async def index(self) -> list[Note]:
        return await self.repository.index()

    async def show(self, hash: str) -> Note:
        return await self.repository.show(hash)

    async def create(self, note: Note) -> Note:
        return await self.repository.create(note)

    async def update(self, hash: str, note: Note) -> Note:
        return await self.repository.update(hash, note)

    async def delete(self, hash: str) -> None:
        return await self.repository.delete(hash)
