import sqlite3
import os
from .models import create_tables
from utils.common import hashlib, fitz

def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    create_tables(conn)
    return conn

# Save document info into the database
def save_document_info(conn, pdfFileObj, pdfReaded, file_name):
    # Connect database
    cursor = conn.cursor()

    # Get the full file path
    file_path = os.path.abspath(file_name)
    # Get the number of pages
    num_pages = len(pdfReaded.pages)
    # Get the width and height of the page
    first_page = pdfReaded.pages[0]
    media_box = first_page.mediabox
    pdf_width = media_box.width
    pdf_height = media_box.height

    # Hash the file name
    file_hash = hashlib.md5(pdfFileObj.read()).hexdigest()

    cursor.execute('''
        INSERT INTO Document (FileName, FilePath, Hashcode, NumPages, Height_px, Width_px)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
    file_name.split('/')[-1], file_path, file_hash, num_pages, int(pdf_height), int(pdf_width)))

    conn.commit()

    return cursor.lastrowid

# Save page info into the database
def save_page_info(conn, doc_id, file_name):
    # Connect database
    cursor = conn.cursor()

    document = fitz.open(file_name)

    # Loop through each page to get margin info
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        rect = page.rect  # Get the rectangle of the page
        # Margins are calculated based on the text box areas within the page
        text_boxes = page.search_for(" ")
        if text_boxes:
            left_margin = min(box.x0 for box in text_boxes) - rect.x0
            right_margin = rect.x1 - max(box.x1 for box in text_boxes)
            top_margin = min(box.y0 for box in text_boxes) - rect.y0
            bottom_margin = rect.y1 - max(box.y1 for box in text_boxes)
        else:
            left_margin = right_margin = top_margin = bottom_margin = 0  # No text found

        # Save the margin info into the database
        cursor.execute('''
            INSERT INTO Page (DocID, PageNum, LeftMargin, RightMargin, TopMargin, BottomMargin)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (int(doc_id), int(page_num + 1), int(left_margin), int (right_margin), int(top_margin), int(bottom_margin)))

        conn.commit()

# Save rectangles into the database
def save_rectangles_info(conn, image_64, info):
    # Connect database
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Rectangle (
        RectID, PageID, DocID, XPos, YPos, Width, Height, Png, LeftAligned, RightAligned, Centered, NumLines, Paragraph_Type, FirstLineIndent, LastLineIndent, MergedPrevRectID, MergedNextRectID, Text_OCR, Text_pyPdf, Text_Nougat, Text_Consolidated, Font_Size, Font_Family, Font_Bold, Font_Italic)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(info["rect_id"]),
            int(info["page_id"]),
            int(info["doc_id"]),
            int(info["x0"]),
            int(info["y0"]),
            int(info["width"]),
            int(info["height"]),
            image_64,
            info["left_aligned"],
            info["right_aligned"],
            info["centered"],
            int(info["num_lines"]),
            info["paragraph_type"],
            info["first_indent"],
            info["last_indent"],
            int(info["merged_prev_rect_id"]),
            int(info["merged_next_rect_id"]),
            info["text_ocr"],
            info["text_pyPdf"],
            info["text_nougat"],
            info["text_consolidated"],
            info["font_size"],
            info["font_family"],
            info["font_bold"],
            info["font_italic"]
        )
    )
    conn.commit()
