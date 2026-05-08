from duckduckgo_search import DDGS


def internet_search(query):

    results_text = []

    with DDGS() as ddgs:

        results = ddgs.text(query, max_results=5)

        for r in results:
            results_text.append(
                f"Title: {r['title']}
"
                f"Body: {r['body']}"
            )

    return "

".join(results_text)