from .common import pytesseract
from .helpers import get_text_font, get_position, get_numlines, process_list

# Get the further info from the element
def get_further_info(element, page_height, doc_id, pagenum, rect_id, text_ocr, text_nougat):
    # Initialize variables
    info = {}
    prev_id = 0
    next_id = 0
    first_indent = last_indent = "N"
    left_aligned = right_aligned = centered = "N"

    # Get font info and text
    text_pyPdf, font_name, font_size, bold, italic = get_text_font(element)

    # Get position of the element
    x0, y0, width, height = get_position(element, page_height)

    # Get num lines of the element
    numlines = get_numlines(element)

    # Check alignment based on the position of lines
    left_positions = process_list([line.x0 for line in element])
    right_positions = process_list([line.x1 for line in element])

    if len(left_positions) == 1 and left_positions[0] == element.x0:
        left_aligned = "Y"
    elif len(right_positions) == 1 and right_positions[0] == element.x1:
        right_aligned = "Y"
    elif len(left_positions) == len(right_positions):
        result = []
        for line in element:
            print(f'Element: {element.x0}, {element.x1} === Line: {line.x0}, {line.x1}')
            result.append(abs(element.x0 - line.x0) == abs(element.x1 - line.x1))

        if len(set(result)) == 1 and result.pop() == True:
            centered = "Y"

    if left_aligned == "N" and right_aligned == "N" and centered == "N" and len(left_positions) == 2:
        if (left_positions[0] > left_positions[1]):
            first_indent = "Y"
        else:
            last_indent = "Y"

    if centered == "N":
        if text_pyPdf and text_pyPdf[0].isupper():
            if not text_pyPdf.endswith(".\n"):
                next_id = rect_id + 1
        elif text_pyPdf and not text_pyPdf[0].islower():
            if text_pyPdf.endswith(".\n"):
                prev_id = rect_id - 1
            else:
                prev_id = rect_id - 1
                next_id = rect_id + 1

    info = {
        'rect_id': rect_id,
        'page_id': pagenum + 1,
        'doc_id': doc_id,
        'x0': x0,
        'y0': y0,
        'width': width,
        'height': height,
        'left_aligned': left_aligned,
        'right_aligned': right_aligned,
        'centered': centered,
        'num_lines': numlines,
        'paragraph_type': 'P',
        'first_indent': first_indent,
        'last_indent': last_indent,
        'merged_prev_rect_id': prev_id,
        'merged_next_rect_id': next_id,
        'text_ocr': text_ocr,
        'text_pyPdf': text_pyPdf,
        'text_nougat': text_nougat,
        'text_consolidated': text_pyPdf,
        'font_size': font_size,
        'font_family': font_name,
        'font_bold': bold,
        'font_italic': italic
    }
    return info

# Get the further info from the figure element
def get_image_further_info(element, page_height, doc_id, pagenum, rect_id, text_ocr, text_nougat):
    # Initialize variables
    info = {}
    prev_id = 0
    next_id = 0
    first_indent = last_indent = "N"
    left_aligned = right_aligned = centered = "N"

    # Get font info and text
    text_pyPdf, font_name, font_size, bold, italic = text_ocr, "", 0, "N", "N"

    # Get position of the element
    x0, y0, width, height = get_position(element, page_height)

    # Get num lines of the element
    numlines = '100'

    info = {
        'rect_id': rect_id,
        'page_id': pagenum + 1,
        'doc_id': doc_id,
        'x0': x0,
        'y0': y0,
        'width': width,
        'height': height,
        'left_aligned': left_aligned,
        'right_aligned': right_aligned,
        'centered': centered,
        'num_lines': numlines,
        'paragraph_type': 'P',
        'first_indent': first_indent,
        'last_indent': last_indent,
        'merged_prev_rect_id': prev_id,
        'merged_next_rect_id': next_id,
        'text_ocr': text_ocr,
        'text_pyPdf': text_pyPdf,
        'text_nougat': text_nougat,
        'text_consolidated': text_pyPdf,
        'font_size': font_size,
        'font_family': font_name,
        'font_bold': bold,
        'font_italic': italic
    }
    return info