from .common import PyPDF2, fitz, Image, base64, io

# Create a function to crop the image elements from PDFs
def crop_image(element, pageObj):
    # Get the coordinates to crop the image from PDF
    [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1]

    # Crop the page using coordinates (left, bottom, right, top)
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    # Save the cropped page to a new PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    # Save the cropped PDF to a new file
    cropped_pdf_path = 'data/cropped_image.pdf'
    with open(cropped_pdf_path, 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Create a function to convert the cropped pdf to image
def convert_to_images(input_file, page_num):
    doc = fitz.open(input_file)
    page = doc.load_page(page_num)  # Load the first page
    pix = page.get_pixmap()
    output_file = 'data/cropped_image.png'
    pix.save(output_file)

# Create a function to convert the PDF to images
def convert_to_images(input_file, ):
    doc = fitz.open(input_file)
    page = doc.load_page(0)  # Load the first page
    pix = page.get_pixmap()
    output_file = 'data/PDF_image.png'
    pix.save(output_file)

# Add margin to the image as a border
def add_margin(image, margin_color=(0, 0, 0)):
    width, height = image.size
    new_image = Image.new('RGB', (width + 2, height + 2), margin_color)
    new_image.paste(image, (1, 1))
    return new_image

# Supporting function to save element as PNG using PyMuPDF
def save_element_as_png(pdf_path, page_num, bbox, doc_id, rect_id):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    page_height = page.rect.height

    # Extract the part of the page corresponding to the bounding box
    zoom = 400.0 / 72.0  # 72 DPI is the default resolution of PDF
    matrix = fitz.Matrix(zoom, zoom)
    clip = fitz.Rect(bbox[0], page_height - bbox[3], bbox[2], page_height - bbox[1])
    pix = page.get_pixmap(matrix=matrix, clip=clip, alpha=False)

    # Convert the pixmap to a PIL Image
    image = Image.open(io.BytesIO(pix.tobytes()))

    # Save the image as a PNG file
    pix.save(f'data/{rect_id}_{page_num+1}_{doc_id}.png')

    # Convert the pixmap to a byte array
    img_bytes = pix.tobytes()

    # Encode the byte array to a base64 string
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    # Close the document
    doc.close()
    return image, img_base64
