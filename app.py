import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
API_KEY = "sk-svcacct-WCXvqS_yg8WxfOt8X-PcbS9I8zwqclC1ZEABPLWS2iNsn5YLyugT6Z_rDszXV5a2T3BlbkFJ_Y64yt49lKiuslf1z7Wh_tTAIy3d3jdJWDpptcssfbwfbY48Aq7OQ82Png2X-MoA"
INDEX_FOLDER = "faiss_index"
METADATA_FILE = "faiss_index/metadata.json"
MAX_HISTORY = 10
K = 5

# Validate API Key
if not API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in the code.")

openai.api_key = API_KEY

# Load FAISS index and metadata
def load_index_and_metadata():
    vector_store = FAISS.load_local(
    INDEX_FOLDER,
    OpenAIEmbeddings(openai_api_key=API_KEY),
    allow_dangerous_deserialization=True
)

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return vector_store, metadata

# Query FAISS index
def query_index(vector_store, query, k):
    return vector_store.similarity_search(query, k=k)

# Summarize results using GPT
def summarize_results_with_gpt(results, query, chat_history):
    combined_content = " ".join([result.page_content.strip() for result in results])
    messages = [
        {"role": "system", "content": "You are a helpful assistant summarizing content clearly in HTML."}
    ]
    messages.extend(
        {"role": role, "content": content} for exchange in chat_history for role, content in exchange.items()
    )
    messages.append({"role": "user", "content": f"Query: '{query}'. Context: {combined_content}"})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()

# Load index and metadata
vector_store, metadata = load_index_and_metadata()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_query = data.get('query', '').strip()
    history = data.get('history', [])

    if not user_query:
        return jsonify({"error": "Empty query provided."}), 400

    results = query_index(vector_store, user_query, k=K)
    if not results:
        return jsonify({"response": "<p>No relevant information found.</p>", "sources": []})

    summarized_response = summarize_results_with_gpt(results, user_query, history)
    sources = [
        f"{idx + 1}. Source: {result.metadata.get('source', 'Unknown')}, Chunk: {result.metadata.get('chunk_index', 'N/A')}"
        for idx, result in enumerate(results)
    ]

    return jsonify({"response": summarized_response, "sources": sources})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
