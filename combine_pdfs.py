import re
from PyPDF2 import PdfReader, PdfWriter
import os

# Define a function to determine the priority of a file
def priority_key(filename):
    # Check if the filename matches the pattern: long string of digits + underscores
    match = re.match(r'^\d+(_[^_]+){3}', filename)
    return (0, filename.lower()) if match else (1, filename.lower())

def custom_sort_key(filename):
    # Check if the filename starts with a two-digit number
    match = re.match(r'^(\d{2})', filename)
    if match:
        return (0, int(match.group(1)))  # Group 1 is the two-digit number
    else:
        return (1, filename)  # Non-matching items come later in natural order

def find_all_pdfs(folder_path, output_file):
    # Get all PDF names
    pdfFiles = [filename for filename in os.listdir(folder_path) if filename.endswith('.pdf')]
    pdfFiles.sort()  # Replace `priority_key` if you have a specific sorting function
    print(pdfFiles)

    pdfWriter = PdfWriter()

    for filename in pdfFiles:
        pdfFileObj = None  # Initialize pdfFileObj to avoid UnboundLocalError
        try:
            file_path = os.path.join(folder_path, filename)  # Ensure correct path
            pdfFileObj = open(file_path, 'rb')
            pdfReader = PdfReader(pdfFileObj)

            # Iterate through pages and add to writer
            for pageNum in range(len(pdfReader.pages)):
                try:
                    pageObj = pdfReader.pages[pageNum]
                    pdfWriter.add_page(pageObj)
                except Exception as e:
                    print(f"Skipping a page in {filename} due to an error: {e}")

        except Exception as e:
            print(f"Skipping {filename} due to an error: {e}")
        finally:
            if pdfFileObj:  # Only close if the file was successfully opened
                pdfFileObj.close()

    # Write the combined PDF
    output_path = os.path.join(os.getcwd(), output_file)
    with open(output_path, 'wb') as pdfOutput:
        pdfWriter.write(pdfOutput)
    print(f"Combined PDF saved as {output_path}")
    return pdfFiles

# change name to do output file
output_file = '2400120_BALTIMORE COUNTY PUBLIC SCHOOLS_09-10-24_CONTRACTS AWARDS.pdf'

folder_path = os.path.join(os.getcwd(), 'pdf')

find_all_pdfs(folder_path, output_file)