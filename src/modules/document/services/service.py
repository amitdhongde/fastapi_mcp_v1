from typing import List

from ..repositories import DocumentRepository
from ..models import Document

class DocumentService:
    def __init__(self):
        self.repository = DocumentRepository()

    async def index(self):
        return await self.repository.index()

    async def show(self, hash: str):
        return await self.repository.show(hash)

    async def create(self, document: Document):
        return await self.repository.create(document)

    async def update(self, hash: str, document: Document):
        return await self.repository.update(hash, document)

    async def delete(self, hash: str):
        return await self.repository.delete(hash)
