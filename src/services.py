import logging
from .highlight_parser_sql import get_book_details, get_books_with_highlights, get_db_path
from .config import ANNOTATION_DB_PATTERN
from .epub_utils import get_epub_metadata
from .markdown_exporter import export_annotations

def export_all_annotations(file_path: str, annotation_type_map: dict) -> None:
    try:
        book_details = get_book_details()
        books_with_highlights = get_books_with_highlights()
    except Exception as e:
        logging.error(f"Error initializing databases: {e}")
        print("An error occurred accessing the Books database.")
        return

    db_path = get_db_path(ANNOTATION_DB_PATTERN)
    for asset_id in books_with_highlights:
        try:
            book_detail = next((bd for bd in book_details if bd.asset_id == asset_id), None)
            if book_detail:
                extra_meta = get_epub_metadata(book_detail.path)
                export_annotations(asset_id, book_detail, file_path, extra_meta, annotation_type_map, db_path)
            else:
                logging.error(f"Book details not found for asset_id: {asset_id}")
        except Exception as e:
            logging.error(f"Error exporting annotations for asset_id {asset_id}: {e}")