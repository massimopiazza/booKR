import os
import glob
import sqlite3
import logging
from typing import List
from .models import BookDetail
from .config import LIBRARY_DB_PATTERN, ANNOTATION_DB_PATTERN

def get_db_path(pattern: str) -> str:
    paths = glob.glob(os.path.expanduser(pattern))
    if not paths:
        raise FileNotFoundError(f"No database found matching pattern: {pattern}")
    return paths[0]

def get_book_details() -> List[BookDetail]:
    try:
        with sqlite3.connect(get_db_path(LIBRARY_DB_PATTERN)) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT ZASSETID, ZSORTTITLE, ZSORTAUTHOR, ZBOOKDESCRIPTION, ZEPUBID, ZPATH
                   FROM ZBKLIBRARYASSET"""
            )
            return [
                BookDetail(
                    asset_id=row[0],
                    title=row[1],
                    author=row[2],
                    description=row[3],
                    epub_id=row[4],
                    path=row[5]
                )
                for row in cursor.fetchall()
            ]
    except sqlite3.Error as e:
        logging.error(f"Database error while retrieving book details: {e}")
        raise

def get_books_with_highlights() -> List[str]:
    book_details = get_book_details()
    book_ids = [book.asset_id for book in book_details]
    if not book_ids:
        return []
    placeholders = ",".join("?" for _ in book_ids)
    try:
        with sqlite3.connect(get_db_path(ANNOTATION_DB_PATTERN)) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""SELECT DISTINCT ZANNOTATIONASSETID
                    FROM ZAEANNOTATION
                    WHERE ZANNOTATIONASSETID IN ({placeholders})
                    AND ZANNOTATIONSELECTEDTEXT != "";""",
                book_ids,
            )
            return [entry[0] for entry in cursor.fetchall()]
    except sqlite3.Error as e:
        logging.error(f"Database error while retrieving annotations: {e}")
        raise