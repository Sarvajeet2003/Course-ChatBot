import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Retrieve configurations from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_FOLDER = os.getenv("INDEX_FOLDER", "faiss_index")
METADATA_FILE = os.getenv("METADATA_FILE", os.path.join(INDEX_FOLDER, "metadata.json"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY", 10))
K = int(os.getenv("K", 5))

# Validate API Key
if not API_KEY:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = API_KEY

def load_index_and_metadata():
    """
    Load the FAISS index and associated metadata.

    Returns:
        tuple: FAISS vector store and metadata dictionary.
    """
    vector_store = FAISS.load_local(
        INDEX_FOLDER,
        OpenAIEmbeddings(openai_api_key=API_KEY),
        allow_dangerous_deserialization=True
    )
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return vector_store, metadata

def query_index(vector_store, query, k=5):
    """
    Query the FAISS index for similar documents.

    Args:
        vector_store (FAISS): The FAISS vector store.
        query (str): The user's query.
        k (int): Number of top results to retrieve.

    Returns:
        list: List of similar document results.
    """
    results = vector_store.similarity_search(query, k=k)
    return results

def summarize_results_with_gpt(results, query, chat_history):
    """
    Summarize the search results using OpenAI's GPT-4, incorporating chat history.

    Args:
        results (list): List of FAISS search results.
        query (str): The current user query.
        chat_history (list): List of previous chat exchanges.

    Returns:
        str: Summarized response in structured HTML format.
    """
    combined_content = " ".join([result.page_content.strip() for result in results])

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes academic and technical content clearly and concisely, formatting output in HTML when appropriate."
        }
    ]

    # Append chat history to messages
    for exchange in chat_history:
        messages.append({"role": "user", "content": exchange["user"]})
        messages.append({"role": "assistant", "content": exchange["assistant"]})

    # Add the current query with the relevant context
    messages.append({
        "role": "user",
        "content": f"Here is the query: '{query}'. Use this context to generate a summarized response:\n{combined_content}"
    })

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()

# Load FAISS index and metadata at startup
vector_store, metadata = load_index_and_metadata()

@app.route('/')
def home():
    """
    Render the main chatbot interface.
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat requests from the frontend.

    Expects JSON payload with:
    - query: The user's input message.
    - history: List of previous chat exchanges.
    """
    data = request.get_json()
    user_query = data.get('query', '').strip()
    history = data.get('history', [])

    if not user_query:
        return jsonify({"error": "Empty query provided."}), 400

    # Query the FAISS index
    results = query_index(vector_store, user_query, k=K)

    if not results:
        return jsonify({
            "response": "<p>I'm sorry, I couldn't find any relevant information.</p>",
            "sources": []
        })

    # Summarize the results
    summarized_response = summarize_results_with_gpt(results, user_query, history)

    # Extract relevant sources
    sources = []
    for idx, result in enumerate(results, start=1):
        source = result.metadata.get("source", "Unknown Source")
        chunk_index = result.metadata.get("chunk_index", "N/A")
        sources.append(f"{idx}. Source: {source}, Chunk Index: {chunk_index}")

    return jsonify({
        "response": summarized_response,
        "sources": sources
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=False)
