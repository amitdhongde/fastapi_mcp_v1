from typing import List

from modules.base.controller import BaseController

from ..services import NoteService
from ..models import Note

class NoteController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = NoteService()

    async def index(self) -> List[Note]:
        return await self.service.index()

    async def show(self, hash: str) -> Note:
        return await self.service.show(hash)

    async def create(self) -> Note:
        return await self.service.create(Note(1, "My Note", "My Note Inc"))

    async def update(self, hash: str) -> Note:
        return await self.service.update(hash, Note(1, "My Note", "My Note Inc"))

    async def delete(self, hash: str):
        return await self.service.delete(hash)
