from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()

loader = DirectoryLoader(
    "knowledge",
    glob="**/*.md"
)

raw_docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(raw_docs)

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com"
)

vector_db = FAISS.from_documents(
    chunks,
    embeddings
)

vector_db.save_local("vectordb")

print("Vector DB updated")