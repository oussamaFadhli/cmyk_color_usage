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
    colors = []

    # Open the PDF file
    doc = fitz.open(pdf_file)

    # Iterate through each page
    for page in doc:
        # Get the raw pixel data
        pix = page.get_pixmap()

        # Extract colors from the pixel data
        for x in range(pix.width):
            for y in range(pix.height):
                r, g, b = pix.pixel(x, y)[:3]  # Get only RGB values
                cmyk = rgb_to_cmyk(r, g, b)
                colors.append(cmyk)

    # Count the occurrence of each color
    color_count = Counter(colors)

    # Calculate the percentage of usage for each color
    total_pixels = sum(color_count.values())
    color_percentage = {color: count / total_pixels * 100 for color, count in color_count.items()}

    return color_percentage

# Humanize input: Ask for the PDF file path
pdf_file = input("Enter the PDF file path: ")

color_info = extract_colors_from_pdf(pdf_file)

# Print color information
for color, percentage in color_info.items():
    print(f"CMYK Color: {color}, Percentage: {percentage:.2f}%")
