# Course-ChatBot

## Overview
Course-ChatBot is an AI-powered chatbot designed to help users retrieve academic regulations from provided PDF documents. The bot processes and extracts relevant information from university course regulations and responds to user queries with precise answers.

## Features
- Extracts text from academic regulation PDFs
- Uses embeddings for better query understanding
- Pre-processes text for efficient search
- Provides accurate responses based on academic regulations

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Sarvajeet2003/Course-ChatBot.git
   cd Course-ChatBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the chatbot:
   ```bash
   python app.py
   ```

## File Structure
- `app.py` - Main script to run the chatbot
- `Data_Extraction.py` - Extracts text from PDFs
- `Embeddings.py` - Generates vector embeddings for document search
- `Pre_processing.py` - Cleans and structures extracted text
- `requirements.txt` - List of dependencies
- `Files/` - Folder containing academic regulation PDFs

## Usage
1. Start the chatbot by running `python app.py`.
2. Enter queries related to course regulations.
3. The chatbot will fetch relevant information from the provided PDFs.

## Future Improvements
- Deploying the chatbot as a web application
- Enhancing response accuracy with advanced NLP models
- Adding support for more document formats

## License
This project is open-source under the MIT License.

## Contributors
- **Sarvajeeth U K** - Developer
