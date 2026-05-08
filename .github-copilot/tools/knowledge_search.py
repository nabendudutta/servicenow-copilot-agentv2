from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com"
)

vector_db = FAISS.load_local(
    "vectordb",
    embeddings,
    allow_dangerous_deserialization=True
)


def search_internal_knowledge(query):

    docs = vector_db.similarity_search_with_score(query, k=4)

    output = []
    scores = []

    for doc, score in docs:
        output.append(doc.page_content)
        scores.append(score)

    avg_score = sum(scores) / len(scores)

    confidence = max(0, int(100 - avg_score))

    return {
        "confidence": confidence,
        "context": "

".join(output)
    }