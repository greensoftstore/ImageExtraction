from .common import pdfplumber, fitz, base64, Image, io

# Extracting tables from the page
def extract_table(pdf_path, doc_id, page_num, rect_id, table_num, dpi = 400):
    # Open the PDF file with pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        # Find the examined page
        table_page = pdf.pages[page_num]
        # Extract the appropriate table
        tables = table_page.extract_tables()
        if not tables or table_num >= len(tables):
            raise ValueError(f"Table number {table_num} not found on page {page_num}.")
        table = tables[table_num]

        # Extract table bounding box
        table_bbox = table_page.find_tables()[table_num].bbox

    # Use PyMuPDF to handle the image extraction
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    page_height = page.rect.height

    # Setting the zoom level for DPI
    zoom = dpi / 72.0  # 72 DPI is the default resolution of PDF
    matrix = fitz.Matrix(zoom, zoom)
    clip = fitz.Rect(table_bbox[0], table_bbox[1], table_bbox[2], table_bbox[3])
    pix = page.get_pixmap(matrix=matrix, clip=clip, alpha=False)

    # Convert the pixmap to a PIL Image
    image = Image.open(io.BytesIO(pix.tobytes()))

    # Save the image as a PNG file
    image_path = f'data/{rect_id}_{page_num+1}_{doc_id}.png'
    pix.save(image_path)

    # Convert the pixmap to a byte array
    img_bytes = pix.tobytes()

    # Encode the byte array to a base64 string
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    # Close the document
    doc.close()

    return table, image, img_base64

# Convert table into appropriate format
def table_converter(table):
    table_string = ''
    # Iterate through each row of the table
    for row_num in range(len(table)):
        row = table[row_num]
        # Remove the line breaker from the wrapted texts
        cleaned_row = [
            item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item
            in row]
        # Convert the table into a string
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    # Removing the last line break
    table_string = table_string[:-1]
    return table_string

# Create a function to check if the element is in any tables present in the page
def is_element_inside_any_table(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

# Function to find the table for a given element
def find_table_for_element(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i  # Return the index of the table
    return None
