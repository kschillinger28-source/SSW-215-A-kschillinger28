import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

# Client created once when module is imported
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ProjectExtraction(BaseModel):
    title: str = Field(description="A short, catchy title for the project.")
    summary: str = Field(description="One or two sentences summarizing the project.")
    technologies: list[str] = Field(description="List of technologies, frameworks, or languages used.")

def extract_project_from_notes(notes: str) -> ProjectExtraction:
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured project details from the user's raw notes."},
            {"role": "user", "content": notes}
        ],
        response_format=ProjectExtraction,
        temperature=0.1
    )
    return response.choices[0].message.parsed