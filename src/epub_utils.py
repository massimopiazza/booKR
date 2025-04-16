import re
from typing import Optional
import logging

def extract_epub_highlight_position_index(cfi: str) -> Optional[int]:
    """
    Extract the child position number from an EPUBCFI string.
    For example, from 'epubcfi(/6/100[id17]!/4,/60/1:484,/70/5:66)' returns 100.
    """
    if cfi.startswith("epubcfi(") and cfi.endswith(")"):
        inner = cfi[len("epubcfi("):-1]
    else:
        inner = cfi
    parts = inner.split("!")
    if not parts:
        return None
    pre = parts[0]
    segments = pre.split("/")
    if len(segments) < 3:
        return None
    m = re.match(r"(\d+)", segments[2])
    return int(m.group(1)) if m else None

def get_epub_metadata(epub_path: str):
    try:
        import ebooklib
        from ebooklib import epub
        import base64

        if not epub_path:
            return None

        book = epub.read_epub(epub_path)
        metadata = {
            "isbn": next((val for _, val in book.get_metadata("DC", "identifier")
                           if isinstance(val, str) and "isbn" in val.lower()), None),
            "language": next((val[0] for val in book.get_metadata("DC", "language")), None),
            "publisher": next((val[0] for val in book.get_metadata("DC", "publisher")), None),
            "publication_date": next((val[0] for val in book.get_metadata("DC", "date")), None),
            "rights": next((val[0] for val in book.get_metadata("DC", "rights")), None),
            "subjects": [val[0] for val in book.get_metadata("DC", "subject")],
        }

        cover_base64 = None
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_COVER:
                cover_data = item.get_content()
                cover_base64 = base64.b64encode(cover_data).decode("utf-8")
                break
        metadata["cover"] = cover_base64
        return metadata

    except ImportError:
        logging.error("ebooklib is not installed. EPUB metadata extraction will not work.")
        return None
    except Exception as e:
        logging.error(f"Error reading EPUB metadata: {e}")
        return None