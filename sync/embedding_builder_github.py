import os
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
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# ============================================
# Create Embeddings using GitHub Models API
# ============================================
github_token = os.getenv("GITHUB_TOKEN")

print(f"DEBUG: GITHUB_TOKEN present = {bool(github_token)}, length = {len(github_token) if github_token else 0}")

if not github_token:
    raise ValueError(
        "GITHUB_TOKEN is None or empty.\n"
        "In GitHub Actions: ensure secret GH_PAT exists and is passed via step env.\n"
        "Locally: ensure GITHUB_TOKEN is set in your .env file."
    )

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=github_token,
    base_url="https://models.inference.ai.azure.com"
)

vector_db = FAISS.from_documents(chunks, embeddings)

# ============================================
# Save Vector DB
# ============================================
vector_db.save_local("vectordb")
print("Vector DB updated successfully")
