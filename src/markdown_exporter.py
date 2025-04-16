import os
import logging
import re
from typing import List, Tuple
from .color_utils import interpolate_palette
from .epub_utils import extract_epub_highlight_position_index
from .models import BookDetail
from .config import ANNOTATION_HEX_PALETTE, MIN_ANNOTATION_LENGTH

def create_file(book_detail: BookDetail, annotations: List[Tuple[str, str, str, str]], file_path: str, extra_meta: dict, annotation_type_map: dict) -> None:
    # merge extra metadata into book details
    if extra_meta:
        book_detail = BookDetail(**{**book_detail.__dict__, **extra_meta})
    try:
        output_md = "---\n"
        for key, value in book_detail.__dict__.items():
            if value and key != "cover":
                output_md += f"{key}: {sanitize_frontmatter(str(value))}\n"
        output_md += "---\n\n"
        output_md += f"# {book_detail.title} by {book_detail.author or 'Unknown'}\n\n"
        if extra_meta and extra_meta.get("cover"):
            output_md += f"![Cover](data:image/jpeg;base64,{extra_meta['cover']})\n\n"
        output_md += "## Metadata\n\n"
        for key, value in book_detail.__dict__.items():
            if key == "path" and value:
                output_md += f"- {key}: [{value}](file://{value})\n"
            elif value and key != "cover":
                output_md += f"- {key}: {value}\n"
        unique_tags = list(annotation_type_map.values())
        colors = interpolate_palette(ANNOTATION_HEX_PALETTE, len(unique_tags))
        tag_color_mapping = {tag: color for tag, color in zip(unique_tags, colors)}
        output_md += "\n## Annotations\n\n"
        prev_child_pos = None
        for highlight, note, location, tag in annotations:
            child_pos = extract_epub_highlight_position_index(location) if location else None
            if prev_child_pos is not None and child_pos is not None and child_pos != prev_child_pos:
                output_md += "\n---\n\n"
            prev_child_pos = child_pos
            color = tag_color_mapping.get(tag, "#000000")
            output_md += f"<div style=\"margin-bottom: 1em;\">\n"
            output_md += f"  <!-- {tag} -->\n"
            output_md += f"  <blockquote style=\"border-left: 4px solid {color}; padding-left: 10px; margin: 0;\">\n"
            for line in highlight.split("\n"):
                output_md += f"    {line}\n"
            output_md += "  </blockquote>\n"
            if note:
                output_md += f"  <p>{note}</p>\n"
            output_md += "</div>\n\n"
        title_sanitized = sanitize_filename(book_detail.title)
        author_sanitized = sanitize_filename(book_detail.author or "Unknown")
        file_name = f"{title_sanitized} - {author_sanitized}.md"
        output_dir = os.path.join(file_path, "output") if file_path else "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.abspath(os.path.join(output_dir, file_name))
        with open(output_path, "w", encoding="utf-8") as mdfile:
            mdfile.write(output_md)
        logging.info(f"Exported annotations for book: {book_detail.title}")
    except IOError as e:
        logging.error(f"Error writing file '{file_name}': {e}")
        raise

def export_annotations(asset_id: str, book_detail: BookDetail, file_path: str, extra_meta: dict, annotation_type_map: dict, db_path: str) -> None:
    import sqlite3
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT ZANNOTATIONSELECTEDTEXT, ZANNOTATIONNOTE, ZANNOTATIONLOCATION, ZANNOTATIONSTYLE
                   FROM ZAEANNOTATION
                   WHERE ZANNOTATIONASSETID = ? AND ZANNOTATIONSELECTEDTEXT != "";""",
                (asset_id,),
            )
            rows = cursor.fetchall()
            filtered_annotations = []
            for selected_text, note, location, ann_style in rows:
                if len(selected_text) < MIN_ANNOTATION_LENGTH:
                    continue
                if ann_style in annotation_type_map:
                    tag = annotation_type_map[ann_style]
                    filtered_annotations.append((selected_text, note, location, tag))
            create_file(book_detail, filtered_annotations, file_path, extra_meta, annotation_type_map)
    except sqlite3.Error as e:
        logging.error(f"Database error while exporting annotations for {asset_id}: {e}")
        raise


def sanitize_frontmatter(text: str) -> str:
    if not text:
        return ""
    replacements = {
        ":": " -",
        "[": "(",
        "]": ")",
        "{": "(",
        "}": ")",
        "#": "",
        "|": "-",
        ">": "-",
        "\\": "/",
        "\n": " ",
        "\r": " ",
    }
    result = str(text)
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    return " ".join(result.split()).strip()

def sanitize_filename(filename: str) -> str:
    # remove invalid characters: <>:"/\\|?*
    return re.sub(r'[<>:"/\\|?*]', '', filename).strip()