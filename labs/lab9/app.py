import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Import your AI service function
from ai_service import extract_project_from_notes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    projects = db.relationship("Project", backref="author")


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False, default="")
    summary = db.Column(db.String(500), nullable=False, default="")          # Added for Lab 9
    technologies = db.Column(db.String(200), nullable=False, default="")    # Added for Lab 9
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "summary": self.summary,
            "technologies": self.technologies,
            "likes": self.likes,
            "author": self.author.name,
        }


def init_seed_data():
    if Project.query.first() is not None:
        return

    author = Author(name="Kurt Schillinger")
    seed_file = Path(__file__).parent / "projects_seed.json"
    if seed_file.exists():
        with seed_file.open("r", encoding="utf-8") as file:
            seed_projects = json.load(file)

        db.session.add(author)
        for seed in seed_projects:
            db.session.add(Project(
                title=seed["title"].strip(),
                description=seed.get("description", ""),
                summary=seed.get("summary", ""),
                technologies=seed.get("technologies", ""),
                likes=seed.get("likes", 0),
                author=author,
            ))

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


with app.app_context():
    db.create_all()
    init_seed_data()


@app.get("/")
def index():
    projects = Project.query.order_by(Project.id).all()
    return render_template("index.html", projects=projects)


@app.get("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(Path(__file__).parent / "assets", filename)


@app.get("/api/projects")
def get_projects():
    projects = Project.query.order_by(Project.id).all()
    return jsonify([project.to_dict() for project in projects]), 200


@app.post("/api/projects")
def create_project():
    data = request.get_json(silent=True)
    title = data.get("title", "").strip() if data else ""
    if not title:
        return jsonify({"error": "Invalid or missing title"}), 400

    author = Author.query.first()
    if author is None:
        return jsonify({"error": "No author is available"}), 400

    new_project = Project(
        title=title,
        description=data.get("description", "").strip(),
        summary=data.get("summary", "").strip(),
        technologies=data.get("technologies", "").strip(),
        likes=0,
        author=author,
    )
    db.session.add(new_project)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A project with that title already exists"}), 400

    return jsonify(new_project.to_dict()), 201


@app.post("/api/projects/smart")
def smart_create_project():
    data = request.get_json(silent=True) or {}
    notes = data.get("notes", "").strip()
    
    # Enforce invariant: Notes shorter than 20 characters must be rejected with 400
    if len(notes) < 20:
        return jsonify({"error": "Notes must be at least 20 characters long."}), 400
        
    try:
        extracted = extract_project_from_notes(notes)
    except Exception as error:
        return jsonify({"error": str(error)}), 503

    author = Author.query.first()
    if author is None:
        return jsonify({"error": "No author is available"}), 400

    tech_str = (
        ", ".join(extracted.technologies)
        if isinstance(extracted.technologies, list)
        else extracted.technologies
    )
    new_project = Project(
        title=extracted.title,
        description=notes,
        summary=extracted.summary,
        technologies=tech_str,
        likes=0,
        author=author,
    )
    db.session.add(new_project)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A project with that title already exists"}), 400

    return jsonify(new_project.to_dict()), 201


@app.post("/api/projects/<int:project_id>/upvote")
def upvote_project(project_id):
    project = db.session.get(Project, project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404

    project.likes += 1
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Unable to update project likes"}), 400

    return jsonify({"likes": project.likes})


if __name__ == "__main__":
    app.run(debug=True, port=5050)