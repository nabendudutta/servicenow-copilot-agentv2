import os
import requests

SNOW_INSTANCE = os.getenv("SNOW_INSTANCE")
SNOW_USER = os.getenv("SNOW_USER")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD")

url = (
    f"https://{SNOW_INSTANCE}.service-now.com/"
    "api/now/table/kb_knowledge"
)

response = requests.get(
    url,
    auth=(SNOW_USER, SNOW_PASSWORD)
)

results = response.json().get("result", [])

os.makedirs("knowledge/servicenow", exist_ok=True)

for item in results:

    number = item.get("number")
    text = item.get("text", "")

    with open(
        f"knowledge/servicenow/{number}.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text)

print("ServiceNow knowledge synced")