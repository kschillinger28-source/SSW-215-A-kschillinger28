from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)

projects_db = [
    {
        "id": 1,
        "title": "Music Discovery App",
        "description": (
            "A Tinder-style swipe interface for discovering songs and curating "
            "playlists."
        ),
        "likes": 8,
    },
    {
        "id": 2,
        "title": "Personal Portfolio",
        "description": (
            "A responsive web portfolio built from a strict Markdown "
            "specification."
        ),
        "likes": 11,
    },
]


@app.get("/")
def index():
    return render_template("index.html", projects=projects_db)


@app.get("/assets/avatar.jpg")
def avatar():
    return send_from_directory(f"{app.root_path}/assets", "avatar.jpg")


@app.route(
    "/api/projects/<int:project_id>/upvote",
    methods=["POST"],
    provide_automatic_options=False,
)
def upvote_project(project_id):
    project = next(
        (item for item in projects_db if item["id"] == project_id),
        None,
    )
    if project is None:
        return jsonify({"error": "Project not found"}), 404

    project["likes"] += 1
    return jsonify({"likes": project["likes"]})


if __name__ == "__main__":
    app.run(debug=True)
