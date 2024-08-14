import sqlite3
import hashlib
import base64
# To read the PDF
import PyPDF2
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextLineHorizontal, LTTextLine, LTTextContainer, LTChar, LTRect, LTFigure, LTImage, LTTextBox

# To extract text from tables in PDF
import pdfplumber

# To extract the images from the PDFs
from PIL import Image

import fitz  # PyMuPDF

# To perform OCR to extract text from images
import pytesseract
# To import for the PDF processing using Nougat
import nougat

import io


__all__ = [
    'sqlite3', 'hashlib', 'base64', 'PyPDF2', 'extract_pages', 'LTTextLineHorizontal', 'LTTextBox', 'LTTextLine', 'LTFigure', 'LTChar', 'LTTextContainer', 'LTImage',
    'LTRect', 'pdfplumber', 'Image', 'pytesseract', 'fitz', 'io', 'nougat'
]
