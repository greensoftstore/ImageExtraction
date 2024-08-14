from .common import fitz, extract_pages, LTTextContainer, LTRect, LTFigure, LTImage, LTTextBox, LTChar

# Create a function to determine if the text element is significant
def is_significant_text(text):
    """Determine if the text element is significant (not just a new line or whitespace)."""
    return text.strip() != ""

# Create a function to draw rectangles on PDF
def draw_rectangles_over_pdf(pdf_path, output_path):
    # Open the original PDF
    doc = fitz.open(pdf_path)
    page_count = len(doc)

    # Iterate through pages in the PDF
    for page_num in range(page_count):
        page = doc.load_page(page_num)

        # Extract elements on the page using pdfminer
        for element in extract_pages(pdf_path, page_numbers=[page_num]):
            for obj in element:
                if isinstance(obj, (LTTextContainer, LTRect, LTFigure, LTImage, LTTextBox)):
                    if isinstance(obj, LTTextContainer) and not is_significant_text(obj.get_text()):
                        continue  # Skip insignificant text elements

                    # Adjust the bounding box coordinates to match PyMuPDF's coordinate system
                    bbox = obj.bbox
                    rect = fitz.Rect(bbox[0], page.rect.height - bbox[3], bbox[2], page.rect.height - bbox[1])
                    # print(rect)

                    # Draw rectangle with red color
                    page.draw_rect(rect, color=(1, 0, 0), width=1)

    # Save the modified PDF
    doc.save(output_path)
    doc.close()

# Process the list
def process_list(list, limit="3"):
    set_list = set(list)
    if len(set_list) == limit:
        # Get the peak value
        peak_value = max(list)
        # Remove the peak value
        list.remove(peak_value)

    # Get the unique values
    seen = set()
    result = []

    # Iterate over the original list
    for item in list:
        if item not in seen:
            result.append(item)
            seen.add(item)

    return result

# Get Font info and text
def get_text_font(element):
    # Extracting the text from the in-line text element
    text = element.get_text()
    # Initialize the font related info
    font_name = ""
    font_size = 0
    bold = "N"
    italic = "N"

    # Find the formats of the text
    # Initialize the list with all the formats appeared in the line of text
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Iterating through each character in the line of text
            for character in text_line:
                if isinstance(character, LTChar):
                    font_name = character.fontname
                    font_size = character.size
                    bold = 'Y' if 'Bold' in font_name else 'N'
                    italic = 'Y' if 'Italic' in font_name or 'Oblique' in font_name else 'N'
                    # Append the info as a tuple
                    line_formats.append((font_name, font_size, bold, italic))

    # Find the unique font sizes and names in the line
    format_per_line = list(set(line_formats))

    # Ensure that format_per_line is not empty before accessing its elements
    if format_per_line:
        first_format = format_per_line[0]
        return text, first_format[0], first_format[1], first_format[2], first_format[3]
    else:
        # Return default values if no formats were found
        return text, font_name, font_size, bold, italic

# Get leftcorner position, width, height of the element
def get_position(element, page_height):
    x0, y0, width, height = element.x0, abs(page_height - element.y1), abs(element.x1 - element.x0), abs(element.y1 - element.y0)
    return x0, y0, width, height

# Get the numlines of the element
def get_numlines(element):
    lines = element.get_text().split('\n')
    return int(len(lines) -1)
