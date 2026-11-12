import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class ProjectExtraction(BaseModel):
    title: str = Field(description="A short, catchy title for the project.")
    summary: str = Field(description="One or two sentences summarizing the project.")
    technologies: list[str] = Field(description="List of technologies, frameworks, or languages used.")


@lru_cache(maxsize=1)
def _get_client() -> Any:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    from openai import OpenAI

    return OpenAI(api_key=api_key, timeout=30.0, max_retries=0)


def extract_project_from_notes(notes: str) -> ProjectExtraction:
    client = _get_client()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured project details from the user's raw notes."},
            {"role": "user", "content": notes},
        ],
        response_format=ProjectExtraction,
        temperature=0.1,
    )
    return response.choices[0].message.parsed