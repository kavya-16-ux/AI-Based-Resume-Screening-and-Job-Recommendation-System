import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

from .skill_extractor import extract_skills, get_missing_skills

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_tokenizer = None
_model = None


def get_model():
    global _tokenizer, _model
    if _tokenizer is None:
        print("[matcher] Loading BERT model (first time only, ~90MB)...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModel.from_pretrained(MODEL_NAME)
        _model.eval()
    return _tokenizer, _model


def _mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * mask, 1) / torch.clamp(mask.sum(1), min=1e-9)


def get_embedding(text: str) -> np.ndarray:
    tokenizer, model = get_model()
    if not text.strip():
        return np.zeros((1, 384))
    encoded = tokenizer(text, padding=True, truncation=True,
                        max_length=512, return_tensors="pt")
    with torch.no_grad():
        output = model(**encoded)
    return _mean_pooling(output, encoded["attention_mask"]).numpy()


def compute_match(resume_text: str, job_description: str) -> dict:
    """Main entry point — returns match score + skills analysis."""
    resume_emb = get_embedding(resume_text)
    job_emb = get_embedding(job_description)
    similarity = float(cosine_similarity(resume_emb, job_emb)[0][0])
    score = round(max(0.0, min(1.0, similarity)) * 100, 2)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    missing = get_missing_skills(resume_skills, job_skills)

    return {
        "match_score": score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing_skills": missing,
    }
