import os
from flask import Flask
import requests

app = Flask(__name__)

GITHUB_USERNAME = "dynamixAI"  # change this if your GitHub handle differs
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

@app.route("/")
def home():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(url, params={"sort": "updated", "per_page": 10}, headers=headers)
    repos = response.json()

    output = "<h1>My GitHub Repos</h1><ul>"
    for repo in repos:
        output += f"<li><a href='{repo['html_url']}'>{repo['name']}</a></li>"
    output += "</ul>"
    return output

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")