import os
import re

# Input and output folders
input_folder = "extracted_texts"
output_folder = "cleaned_texts"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def clean_text(text):
    # Remove excessive newlines and special characters
    text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with one
    text = re.sub(r'[^\S\r\n]+', ' ', text)  # Replace multiple spaces with one
    text = text.strip()  # Remove leading/trailing whitespace
    return text

def preprocess_all_files(input_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):  # Process only text files
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            print(f"Processing: {file_name}")
            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            cleaned_text = clean_text(raw_text)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            print(f"Saved cleaned text: {output_path}")

if __name__ == "__main__":
    preprocess_all_files(input_folder)
