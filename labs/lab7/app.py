import json
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__)

#Build the right path to projects.json relative to app.py
DATA_FILE = Path(__file__).parent / "projects.json"


def load_projects():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_projects(projects):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2)


@app.get("/")
def index():
    projects = load_projects()
    return render_template("index.html", projects=projects)


@app.get("/assets/avatar.jpg")
def avatar():
    return send_from_directory(f"{app.root_path}/assets", "avatar.jpg")


@app.post("/api/projects")
def create_project():
    data = request.get_json()
    if not data or not data.get("title", "").strip():
        return jsonify({"error": "Invalid or missing title"}), 400

    projects = load_projects()

    # Calculate next ID
    max_id = max((p["id"] for p in projects), default=0)
    new_id = max_id + 1

    new_project = {
        "id": new_id,
        "title": data["title"].strip(),
        "description": data.get("description", ""),
        "likes": 0
    }

    projects.append(new_project)
    save_projects(projects)

    return jsonify(new_project), 201


@app.route(
    "/api/projects/<int:project_id>/upvote",
    methods=["POST"],
    provide_automatic_options=False,
)
def upvote_project(project_id):
    projects = load_projects()
    project = next(
        (item for item in projects if item["id"] == project_id),
        None,
    )
    if project is None:
        return jsonify({"error": "Project not found"}), 404

    project["likes"] += 1
    save_projects(projects)
    return jsonify({"likes": project["likes"]})


if __name__ == "__main__":
    app.run(debug=True)