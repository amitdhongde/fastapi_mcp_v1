from typing import List

from ..services import DocumentService
from ..models import Document

from modules.base.controller import BaseController

class DocumentController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = DocumentService()

    async def index(self) -> List[Document]:
        return await self.service.index()

    async def show(self, hash: str) -> Document:
        return await self.service.show(hash)

    async def create(self) -> Document:
        return await self.service.create(Document(1, "Sample Document", "sample@document.com"))

    async def update(self, hash: str) -> Document:
        return await self.service.update(hash, Document(1, "Sample Document", "sample@document.com"))

    async def delete(self, hash: str) -> None:
        return await self.service.delete(hash)
    