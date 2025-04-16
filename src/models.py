from typing import List, Optional
from dataclasses import dataclass

@dataclass
class BookDetail:
    asset_id: str
    title: str
    author: Optional[str]
    description: Optional[str]
    epub_id: Optional[str]
    path: Optional[str]
    isbn: Optional[str] = None
    language: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[str] = None
    rights: Optional[str] = None
    subjects: Optional[List[str]] = None
    cover: Optional[str] = None