import json
import os
from difflib import SequenceMatcher

CACHE_FILE = ".github-copilot/cache/query_cache.json"


class Memory:

    def __init__(self):

        os.makedirs(
            ".github-copilot/cache",
            exist_ok=True
        )

        if not os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "w") as f:
                json.dump([], f)

    def load(self):

        with open(CACHE_FILE, "r") as f:
            return json.load(f)

    def save(self, query, answer):

        data = self.load()

        data.append({
            "query": query,
            "answer": answer
        })

        with open(CACHE_FILE, "w") as f:
            json.dump(data[-200:], f, indent=2)

    def find(self, query):

        data = self.load()

        for item in data:

            similarity = SequenceMatcher(
                None,
                query.lower(),
                item["query"].lower()
            ).ratio()

            if similarity > 0.90:
                return item["answer"]

        return None