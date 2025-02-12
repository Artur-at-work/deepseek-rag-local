import os
import streamlit as st
import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.embeddings import HuggingFaceEmbeddings  # deprecated

# Configuration
CODE_DIR = "./my_codebase"  # Your dir with github repositories
VECTOR_DB_PATH = "faiss_index"

# Load Embeddings Model
#embedder = HuggingFaceEmbeddings() # deprecated
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Function to Index Codebase
def index_codebase():
    st.info("Indexing codebase... This may take a while.")

    # Check if CODE_DIR exists, create if not
    if not os.path.exists(CODE_DIR):
        os.makedirs(CODE_DIR)
        print(f"Created new directory: {CODE_DIR}")
        st.warning(f"No files found in {CODE_DIR}. Please add files to index.")
        return

    # Load all code files recursively from each directory
    loader = DirectoryLoader(CODE_DIR, glob="**/*.{py,sh,yaml,yml,json,md}", show_progress=True)
    docs = loader.load()

    # Split into chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    # Create FAISS Vector Store
    faiss_db = FAISS.from_documents(chunks, embedder)
    faiss_db.save_local(VECTOR_DB_PATH)

    st.success("Indexing complete!")

# Load Vector Store
def load_vector_store():
    return FAISS.load_local(VECTOR_DB_PATH, embedder, allow_dangerous_deserialization=True)

# Retrieve Code Snippets
def retrieve_code(query, top_k=3):
    faiss_db = load_vector_store()
    results = faiss_db.similarity_search(query, k=top_k)
    return "\n\n".join([r.page_content for r in results])

# Streamlit UI
st.set_page_config(page_title="POC Local DeepSeek RAG", layout="wide")
st.title("Deepseek runs locally with RAG codebase")

# Index Codebase Button
if st.button("Learn Codebase"):
    index_codebase()

# User Query Input
query = st.text_input("Ask a question about the codebase:")

if query:
    # Retrieve relevant code
    context = retrieve_code(query)
    st.markdown("### Retrieved Code Context")
    st.code(context)

    # Query DeepSeek with Augmented Context
    full_query = f"Context:\n{context}\n\nQuery:\n{query}"
    response = ollama.chat(model="deepseek-r1", messages=[{"role": "user", "content": full_query}])
    # TODO: a better prompt to make the model understand the context better

    # Display Response
    if hasattr(response, "message") and hasattr(response.message, "content"):
        answer = response.message.content
    else:
        answer = str(response)

    st.markdown("### DeepSeek Response")
    st.markdown(answer)