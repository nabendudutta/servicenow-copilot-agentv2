import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN is not set. Add it to your .env file or environment.")
# ============================================
# Load Markdown Files
# ============================================

documents = []

for root, dirs, files in os.walk("knowledge"):

    for file in files:

        if file.endswith(".md"):

            path = os.path.join(root, file)

            try:

                loader = TextLoader(
                    path,
                    encoding="utf-8"
                )

                documents.extend(
                    loader.load()
                )

                print(f"Loaded: {path}")

            except Exception as e:

                print(f"Failed loading {path}: {e}")

# ============================================
# Split Documents
# ============================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# ============================================
# Create Embeddings using GitHub Models API
# ============================================

# Using GitHub's model inference API with text-embedding-3-small
# This requires GITHUB_TOKEN to be set in your environment
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com"
)

# Alternative: text-embedding-3-large for better quality (uncomment to use)
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-3-large",
#     api_key=os.getenv("GITHUB_TOKEN"),
#     base_url="https://models.inference.ai.azure.com"
# )

vector_db = FAISS.from_documents(
    chunks,
    embeddings
)

# ============================================
# Save Vector DB
# ============================================

vector_db.save_local("vectordb")

print("Vector DB updated successfully")
