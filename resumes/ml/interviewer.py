from sentence_transformers import SentenceTransformer, util

# Load the same lightweight model used for resume matching
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_interview_questions(missing_skills_str):
    # Convert string "Python, SQL" to list ["Python", "SQL"]
    skills = [s.strip() for s in missing_skills_str.split(",") if s.strip()]
    
    questions = []
    for skill in skills[:5]:  # Ask up to 5 questions
        questions.append({
            "question": f"Explain the core concepts of {skill} and how you would implement it in a real-world project.",
            "ideal_answer": f"The candidate should describe the fundamental principles of {skill}, mention specific libraries or tools associated with it, and provide a logical project use-case."
        })
    return questions

def calculate_answer_score(candidate_answer, ideal_answer):
    if not candidate_answer: return 0
    
    # Generate embeddings (vectors) for both answers
    embeddings = model.encode([candidate_answer, ideal_answer], convert_to_tensor=True)
    
    # Calculate Cosine Similarity
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    return round(max(0, similarity * 100), 2)