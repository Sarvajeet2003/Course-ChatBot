import os
from PyPDF2 import PdfReader

# Path to the folder containing PDFs
pdf_folder = "Files"  # Replace with your folder path
output_folder = "extracted_texts"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Extract text page by page
        return text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return ""

def process_all_pdfs(pdf_folder):
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(pdf_folder, file_name)
            print(f"Processing: {file_name}")
            text = extract_text_from_pdf(pdf_path)
            
            # Save extracted text to a .txt file
            output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    process_all_pdfs(pdf_folder)
