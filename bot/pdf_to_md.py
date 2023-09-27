import os
import aspose.words as aw

# Define the input and output directories
input_directory = "./data/pdfs/"
output_directory = "./data/md/"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)


# Loop through PDF files in the input directory
def convert_pdf_to_md():
    for filename in os.listdir(input_directory):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_directory, filename)
            output_filename = os.path.splitext(filename)[0] + ".md"
            output_path = os.path.join(output_directory, output_filename)

            # Use pdfminer.high_level.extract_text to extract text from PDF
            doc = aw.Document(input_path)

            doc.save(output_path)
