import os
from db.utils import initialize_db, save_document_info, save_page_info, save_rectangles_info
from utils.common import PyPDF2, pdfplumber, extract_pages, LTTextContainer, LTRect, LTFigure, LTImage, pytesseract
from utils.extract import get_further_info, get_image_further_info
from utils.table import extract_table, table_converter, is_element_inside_any_table, find_table_for_element
from utils.image import crop_image, convert_to_images, save_element_as_png
from utils.ocr import image_to_text, ocr_text
from utils.nougat import nougat_text
from utils.helpers import is_significant_text

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Main Function
def main(file_name, db_path, lang='eng'):
    # Initialize the database
    db_conn = initialize_db(db_path)

    # Create a pdf file object
    pdfFileObj = open(file_name, 'rb')
    # Create a pdf reader object
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)

    doc_id = save_document_info(db_conn, pdfFileObj, pdfReaded, file_name)

    # Save the page info into the database
    save_page_info(db_conn, doc_id, file_name)

    # Create a boolean variable for image detection
    image_flag = False
    # Create a boolean variable for previous image element detection
    prev_image_flag = False

    # Open the pdf file
    pdf = pdfplumber.open(file_name)

    # Set RectID to 1
    rect_id = 1

    # We extract the pages from the PDF
    for pagenum, page in enumerate(extract_pages(file_name)):
        page_height = page.height

        # Initialize the variables needed for the text extraction from the page
        pageObj = pdfReaded.pages[pagenum]

        page_content = []
        # Initialize the number of the examined tables
        table_in_page = -1

        # Find the examined page
        page_tables = pdf.pages[pagenum]
        # Find the number of tables in the page
        tables = page_tables.find_tables()
        if len(tables) != 0:
            table_in_page = 0

        # Extracting the tables of the page
        for table_num in range(len(tables)):
            # Extract the information of the table
            table, pil_image, base64_image = extract_table(file_name, doc_id, pagenum, rect_id, table_num)

            # Convert the table information in structured string format
            table_string = table_converter(table)

            # Use pytesseract to extract text from the PIL Image
            text_ocr = ocr_text(pil_image)

            rect_id += 1

        # Find all the elements
        page_elements = [element for element in page._objs]

        # Find the elements that composed a page
        for i, component in enumerate(page_elements):
            # Extract the element of the page layout
            element = component

            # Check the elements for tables
            if table_in_page == -1:
                pass
            else:
                if is_element_inside_any_table(element, page, tables):
                    table_found = find_table_for_element(element, page, tables)
                    if table_found == table_in_page and table_found != None:
                        table_in_page += 1
                    # Pass this iteration because the content of this element was extracted from the tables
                    continue

            if not is_element_inside_any_table(element, page, tables):
                # Check if the element is text element
                if isinstance(element, LTTextContainer) and not isinstance(element, LTRect) and is_significant_text(element.get_text()):
                    # Extract the bounding box of the element
                    bbox = (element.x0, element.y0, element.x1, element.y1)
                    # Save the element as a PNG file using PyMuPDF
                    image, image_64 = save_element_as_png(file_name, pagenum, bbox, doc_id, rect_id)
                    # Get text using OCR
                    text_ocr = ocr_text(image)
                    # Get text using Nougat
                    text_nougat = nougat_text(image)
                    # Get info of the element to save it in the database
                    info = get_further_info(element, page_height, doc_id, pagenum, rect_id, text_ocr, text_nougat)
                    # Save rectangle data into the database
                    save_rectangles_info(db_conn, image_64, info)
                    rect_id += 1

                # Check the elements for images
                if isinstance(element, LTFigure) or isinstance(element, LTImage):
                    # Extract the bounding box of the element
                    bbox = (element.x0, element.y0, element.x1, element.y1)
                    # Save the element as a PNG file using PyMuPDF
                    image, image_64 = save_element_as_png(file_name, pagenum, bbox, doc_id, rect_id)
                    # Get text using OCR
                    text_ocr = ocr_text(image)
                    # Get text using Nougat
                    text_nougat = nougat_text(image)
                    # Get info of the element to save it in the database
                    info = get_image_further_info(element, page_height, doc_id, pagenum, rect_id, text_ocr, text_nougat)
                    # Save the text into the database
                    save_rectangles_info(db_conn, image_64, info)
                    rect_id += 1
                    # Update the flag for image detection
                    image_flag = True                    # prev_image_flag = True

    # Close the pdf file object
    pdfFileObj.close()
    pdf.close()

    db_conn.close()

# Run the process with a sample PDF file
if __name__ == "__main__":
    main('data/Exam.pdf', 'data/paper.db', 'eng+spa')  # Specify the languages as needed