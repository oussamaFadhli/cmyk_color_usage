import fitz
from collections import Counter
from colorsys import rgb_to_yiq

def rgb_to_cmyk(r, g, b):
    """
    Convert RGB color to CMYK color
    """
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    if k == 1:
        return 0, 0, 0, 1
    return (c - k) / (1 - k), (m - k) / (1 - k), (y - k) / (1 - k), k

def extract_colors_from_pdf(pdf_file):
    cmyk_summary = {
        'Cyan': 0,
        'Magenta': 0,
        'Yellow': 0,
        'Black': 0
    }

    # Open the PDF file
    doc = fitz.open(pdf_file)
    
    num_pages = len(doc)  # Get the number of pages

    # Iterate through each page
    for page in doc:
        # Get the raw pixel data
        pix = page.get_pixmap()

        # Extract colors from the pixel data
        for x in range(pix.width):
            for y in range(pix.height):
                r, g, b = pix.pixel(x, y)[:3]  # Get only RGB values
                c, m, y, k = rgb_to_cmyk(r, g, b)
                cmyk_summary['Cyan'] += c
                cmyk_summary['Magenta'] += m
                cmyk_summary['Yellow'] += y
                cmyk_summary['Black'] += k

    total_pixels = pix.width * pix.height * num_pages

    # Calculate percentages
    for key in cmyk_summary:
        cmyk_summary[key] = cmyk_summary[key] / total_pixels * 100

    return cmyk_summary, num_pages

# Humanize input: Ask for the PDF file path
pdf_file = input("Enter the PDF file path: ")

color_summary, num_pages = extract_colors_from_pdf(pdf_file)

# Print output name and number of pages
print(f"PDF file: {pdf_file}")
print(f"Number of pages: {num_pages}")

# Print color summary
for key, value in color_summary.items():
    print(f"{key}: {value:.2f}%")
