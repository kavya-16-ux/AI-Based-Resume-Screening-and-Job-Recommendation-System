import spacy
from .skills_db import SKILLS_DB

_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def extract_skills(text: str) -> list:
    """Extract skills from text using spaCy + SKILLS_DB matching."""
    if not text:
        return []

    nlp = get_nlp()
    doc = nlp(text.lower())
    tokens = {t.text for t in doc if not t.is_punct}
    text_lower = text.lower()

    found = set()
    for skill in SKILLS_DB:
        s = skill.lower()
        if " " in s or "." in s or "/" in s or "+" in s:
            if s in text_lower:
                found.add(s)
        else:
            if s in tokens:
                found.add(s)
    return sorted(found)


def get_missing_skills(resume_skills: list, job_skills: list) -> list:
    return sorted(set(job_skills) - set(resume_skills))
