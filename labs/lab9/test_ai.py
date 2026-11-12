from ai_service import extract_project_from_notes

notes = "We built a full-stack recipe sharing app using React, Flask, and PostgreSQL where users can upload photos."
result = extract_project_from_notes(notes)
print(result)