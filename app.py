import os
from flask import Flask, render_template
import requests

app = Flask(__name__)

GITHUB_USERNAME = "dynamixAI"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
DISPLAY_NAME = "Pius Ajamma"


@app.route("/")
def home():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    response = requests.get(
        url,
        params={"sort": "updated", "per_page": 10},
        headers=headers,
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

    repos = []

    for repo in data:
        repos.append({
            "name": repo["name"],
            "description": repo["description"] or "No description yet.",
            "language": repo["language"] or "N/A",
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
            "updated_at": repo["updated_at"],
        })

    total_stars = sum(r["stars"] for r in repos)

    languages = {}

    for r in repos:
        languages[r["language"]] = languages.get(r["language"], 0) + 1

    return render_template(
        "index.html",
        username=GITHUB_USERNAME,
        display_name=DISPLAY_NAME,
        repos=repos,
        total_stars=total_stars,
        chart_labels=list(languages.keys()),
        chart_values=list(languages.values()),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")