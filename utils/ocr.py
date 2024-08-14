from .common import Image, pytesseract

# Create a function to read text from images
def image_to_text(image_path):
    # Read the image
    img = Image.open(image_path)
    # Extract the text from the image
    text = pytesseract.image_to_string(img)
    return text

# Get the text from Image
def ocr_text(image):
    # Use pytesseract to extract text from the PIL Image
    text = pytesseract.image_to_string(image)
    return text