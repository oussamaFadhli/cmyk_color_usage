import fitz
import numpy as np

def extract_colors_from_pdf(pdf_file):
    cmyk_summary = {
        'cyan': 0,
        'magenta': 0,
        'yellow': 0,
        'black': 0
    }

    # Open the PDF file
    doc = fitz.open(pdf_file)
    num_pages = len(doc)  # Get the number of pages

    for page in doc:
        # Get the raw pixel data
        pix = page.get_pixmap()
        # Convert pixmap to numpy array
        img_data = np.frombuffer(pix.samples, dtype=np.uint8)
        img_data = img_data.reshape((pix.height, pix.width, pix.n))

        # Convert RGB to CMYK
        img_data = img_data[:, :, :3]  # Exclude alpha channel if present
        cmyk_data = 1 - img_data / 255
        k = np.min(cmyk_data, axis=2)
        cmyk_data = (cmyk_data - k[:, :, None]) / (1 - k[:, :, None] + 1e-10)

        # Update summary
        cmyk_summary['cyan'] += np.sum(cmyk_data[:, :, 0])
        cmyk_summary['magenta'] += np.sum(cmyk_data[:, :, 1])
        cmyk_summary['yellow'] += np.sum(cmyk_data[:, :, 2])
        cmyk_summary['black'] += np.sum(k)

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
