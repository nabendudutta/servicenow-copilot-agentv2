import os
import time
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# ============================================
# Load Markdown Files
# ============================================
documents = []

for root, dirs, files in os.walk("knowledge"):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            try:
                loader = TextLoader(path, encoding="utf-8")
                documents.extend(loader.load())
                print(f"Loaded: {path}")
            except Exception as e:
                print(f"Failed loading {path}: {e}")

if not documents:
    raise ValueError("No markdown files found in the 'knowledge' directory.")

# ============================================
# Split Documents
# ============================================
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# ============================================
# Create Embeddings using GitHub Models API
# ============================================
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    raise ValueError(
        "GITHUB_TOKEN is None or empty.\n"
        "In GitHub Actions: ensure secret GH_PAT exists and is passed via step env.\n"
        "Locally: ensure GITHUB_TOKEN is set in your .env file."
    )

print(f"DEBUG: GITHUB_TOKEN present = {bool(github_token)}, length = {len(github_token)}")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=github_token,
    base_url="https://models.inference.ai.azure.com"
)

# ============================================
# Batch chunks to stay under 64k token limit
# ============================================
BATCH_SIZE = 50  # ~50 chunks per request, safe for 64k token limit

def batch_chunks(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]

vector_db = None

for i, batch in enumerate(batch_chunks(chunks, BATCH_SIZE)):
    print(f"Embedding batch {i + 1} / {-(-len(chunks) // BATCH_SIZE)} ({len(batch)} chunks)...")
    
    if vector_db is None:
        vector_db = FAISS.from_documents(batch, embeddings)
    else:
        vector_db.add_documents(batch)
    
    time.sleep(0.5)  # avoid rate limiting

# ============================================
# Save Vector DB
# ============================================
vector_db.save_local("vectordb")
print("Vector DB updated successfully")