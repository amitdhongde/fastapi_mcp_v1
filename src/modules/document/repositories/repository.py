#from modules.core.repository.base import BaseRepository
from modules.document.models import Document

class DocumentRepository():
    def __init__(self):
        #super().__init__(Document)
        pass

    async def index(self):
        return 'DocumentRepository index'

    async def show(self, hash: str):
        return f'DocumentRepository show {hash}'

    async def create(self, document: Document):
        return 'DocumentRepository create'

    async def update(self, hash: str, document: Document):
        return f'DocumentRepository update {hash}'

    async def delete(self, hash: str):
        return f'DocumentRepository delete {hash}'
    