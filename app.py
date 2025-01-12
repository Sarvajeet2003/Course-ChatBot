import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
import os
import json

# Set your OpenAI API key
API_KEY = "sk-svcacct-WCXvqS_yg8WxfOt8X-PcbS9I8zwqclC1ZEABPLWS2iNsn5YLyugT6Z_rDszXV5a2T3BlbkFJ_Y64yt49lKiuslf1z7Wh_tTAIy3d3jdJWDpptcssfbwfbY48Aq7OQ82Png2X-MoA"  # Replace with your API key
openai.api_key = API_KEY

# Paths
INDEX_FOLDER = "faiss_index"
METADATA_FILE = os.path.join(INDEX_FOLDER, "metadata.json")

# Load FAISS index and metadata
def load_index_and_metadata():
    vector_store = FAISS.load_local(INDEX_FOLDER, OpenAIEmbeddings(openai_api_key=API_KEY), allow_dangerous_deserialization=True)
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return vector_store, metadata

# Query FAISS index and fetch relevant results
def query_index(vector_store, query, k=5):
    results = vector_store.similarity_search(query, k=k)
    return results

# Summarize results with GPT
# Summarize results with GPT
def summarize_results_with_gpt(results, query):
    combined_content = ""
    for result in results:
        combined_content += f"{result.page_content.strip()} "
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes academic and technical content clearly and concisely."},
                {"role": "user", "content": f"Here is the query: '{query}'. Use this context to generate a summarized response:\n{combined_content}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error during summarization: {e}"



# Streamlit App
st.title("Academic Chatbot")
st.write("Ask a question and get summarized academic or technical responses!")

# Load index and metadata
st.write("Loading the FAISS index... Please wait.")
vector_store, metadata = load_index_and_metadata()

# User input
query = st.text_input("Enter your query:", placeholder="Type your academic or technical question here")

if st.button("Get Answer"):
    if query.strip():
        with st.spinner("Querying the index and generating a response..."):
            # Query the FAISS index
            results = query_index(vector_store, query)

            # Summarize the results
            summarized_response = summarize_results_with_gpt(results, query)

            # Display results
            st.subheader("Summarized Response")
            st.write(summarized_response)

            st.subheader("Relevant Sources")
            for idx, result in enumerate(results, start=1):
                source = result.metadata["source"]
                chunk_index = result.metadata["chunk_index"]
                st.write(f"{idx}. **Source**: {source}, **Chunk Index**: {chunk_index}")
    else:
        st.warning("Please enter a query to get a response.")
