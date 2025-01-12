import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

# Initialize OpenAI Embeddings
API_KEY = "sk-svcacct-WCXvqS_yg8WxfOt8X-PcbS9I8zwqclC1ZEABPLWS2iNsn5YLyugT6Z_rDszXV5a2T3BlbkFJ_Y64yt49lKiuslf1z7Wh_tTAIy3d3jdJWDpptcssfbwfbY48Aq7OQ82Png2X-MoA" # Replace with your OpenAI API Key  # Replace with your actual API key
embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)

# Paths
CLEANED_FOLDER = "cleaned_texts"
INDEX_FOLDER = "faiss_index"
METADATA_FILE = os.path.join(INDEX_FOLDER, "metadata.json")

# Split text into chunks for embeddings
def create_chunks(text, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)

# Save metadata for later use
def save_metadata(metadata):
    os.makedirs(INDEX_FOLDER, exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to {METADATA_FILE}")

# Build FAISS index
def build_faiss_index(cleaned_folder):
    documents = []
    metadata = []

    # Iterate through cleaned text files
    for file_name in os.listdir(cleaned_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(cleaned_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            # Create chunks
            chunks = create_chunks(raw_text)
            documents.extend(chunks)
            
            # Metadata includes source file and chunk index
            metadata.extend(
                [{"source": file_name, "chunk_index": idx} for idx in range(len(chunks))]
            )
    
    print("Creating embeddings and storing in FAISS index...")
    
    # Create vector store with metadata
    vector_store = FAISS.from_texts(documents, embeddings, metadatas=metadata)
    vector_store.save_local(INDEX_FOLDER)
    
    # Save metadata separately for reference
    save_metadata(metadata)
    print(f"FAISS index saved locally at '{INDEX_FOLDER}'")

if __name__ == "__main__":
    build_faiss_index(CLEANED_FOLDER)
