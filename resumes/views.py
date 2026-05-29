import fitz  # PyMuPDF
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions

from .models import Resume, AIInterview, InterviewQuestion
from .serializers import ResumeSerializer
from jobs.models import Job
from applications.models import Application
from ml.matcher import compute_match 
from .ml.interviewer import generate_interview_questions, calculate_answer_score

# --- 1. CONFIG & HELPERS ---

COMMON_SKILLS = [
    "python", "django", "flask", "fastapi", "javascript", "react",
    "html", "css", "bootstrap", "sql", "postgresql", "mysql",
    "machine learning", "deep learning", "nlp", "tensorflow",
    "pytorch", "pandas", "numpy", "git", "docker", "aws"
]

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"Extraction Error: {e}")
        return ""

def extract_skills_from_text(text):
    text_lower = text.lower()
    found_skills = [skill.title() for skill in COMMON_SKILLS if skill in text_lower]
    return sorted(list(set(found_skills)))

def generate_roadmap_logic(all_recommendations):
    """
    Analyzes gaps across ALL jobs to find high-impact skills.
    """
    roadmap = []
    global_missing_skills = {}
    
    for item in all_recommendations:
        for skill in item.get('missing_skills', []):
            skill_key = skill.lower()
            global_missing_skills[skill_key] = global_missing_skills.get(skill_key, 0) + 1

    sorted_skills = sorted(global_missing_skills.items(), key=lambda x: x[1], reverse=True)
    
    skill_data = {
        "django": "Master backend architectures and RESTful APIs.",
        "postgresql": "Learn advanced database management and relational modeling.",
        "react": "Build interactive user interfaces and manage complex states.",
        "aws": "Understand cloud infrastructure and scalable deployments.",
        "docker": "Implement containerization for seamless environment control."
    }

    for skill_name, frequency in sorted_skills[:3]:
        name = skill_name.title()
        desc = skill_data.get(skill_name, f"This skill is required by {frequency} roles in your match list.")
        roadmap.append({
            "step": f"Master {name}",
            "desc": desc,
            "icon": "fa-layer-group"
        })

    if not roadmap:
        roadmap.append({
            "step": "Advanced System Design",
            "desc": "Focus on architectural patterns and scalability.",
            "icon": "fa-microchip"
        })

    return roadmap

# --- 2. CANDIDATE VIEWS ---

@login_required
def candidate_dashboard(request):
    resume = Resume.objects.filter(user=request.user).first()
    applications = Application.objects.filter(user=request.user).select_related("job")
    latest_interview = AIInterview.objects.filter(candidate=request.user, completed=True).order_by("-created_at").first()
    
    recommendations = []
    roadmap = []           
    target_score = 0      
    current_top_score = 0 
    target_job_title = "General Tech"

    if resume and resume.extracted_text:
        for job in Job.objects.all():
            job_full_text = f"{job.title} {job.description}"
            match_results = compute_match(resume.extracted_text, job_full_text)
            
            recommendations.append({
                "job": job,
                "score": match_results.get("match_score", 0),
                "missing_skills": match_results.get("missing_skills", [])
            })
        
        recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)[:5]
        
        if recommendations:
            roadmap = generate_roadmap_logic(recommendations)
            roadmap_source = next((item for item in recommendations if item['missing_skills']), recommendations[0])
            
            m_skills = roadmap_source.get('missing_skills', [])
            current_top_score = roadmap_source.get('score', 0)
            target_job_title = roadmap_source['job'].title
            
            boost = len(roadmap) * 10
            target_score = min(98.5, current_top_score + boost)
            request.session['current_missing_skills'] = ", ".join(m_skills) if m_skills else "General Tech"

    return render(request, "candidate/dashboard.html", {
        "resume": resume,
        "applications": applications,
        "recommendations": recommendations,
        "latest_interview": latest_interview,
        "roadmap": roadmap,         
        "target_score": round(target_score, 2), 
        "current_score": round(current_top_score, 2),
        "target_job_title": target_job_title
    })

@login_required
def upload_resume_page(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("resume")
        if not uploaded_file:
            messages.error(request, "Please upload a PDF file.")
            return redirect("upload-resume")

        resume, _ = Resume.objects.get_or_create(user=request.user)
        resume.file = uploaded_file
        resume.save()

        text = extract_text_from_pdf(resume.file.path)
        resume.extracted_text = text
        resume.extracted_skills = extract_skills_from_text(text)
        resume.save()

        messages.success(request, "Resume processed successfully!")
        return redirect("candidate-dashboard")

    return render(request, "candidate/upload_resume.html")

# --- 3. AI INTERVIEW & CERTIFICATE ---

@login_required
def start_ai_interview(request):
    missing_skills = request.session.get("current_missing_skills")
    if not missing_skills or missing_skills.strip() == "":
        missing_skills = "Python, Web Development, SQL"
    
    interview = AIInterview.objects.create(
        candidate=request.user, 
        missing_skills=missing_skills
    )
    
    questions_data = generate_interview_questions(missing_skills)
    
    if not questions_data:
        questions_data = [
            {"question": f"Explain your proficiency with {missing_skills.split(',')[0]}.", 
             "ideal_answer": "Candidate should demonstrate core understanding."},
            {"question": "Describe a major technical challenge you faced.", 
             "ideal_answer": "Systematic problem solving and debugging skills."}
        ]

    for q in questions_data:
        InterviewQuestion.objects.create(
            interview=interview,
            question=q["question"],
            ideal_answer=q["ideal_answer"]
        )
    return redirect("ai_interview", interview_id=interview.id)

@login_required
def ai_interview(request, interview_id):
    interview = get_object_or_404(AIInterview, id=interview_id, candidate=request.user)
    questions = interview.questions.all()

    if request.method == "POST":
        total_score = 0
        for q in questions:
            ans = request.POST.get(f"answer_{q.id}", "")
            q.candidate_answer = ans
            q.score = calculate_answer_score(ans, q.ideal_answer)
            q.save()
            total_score += q.score
        
        if questions.exists():
            interview.total_score = round(total_score / questions.count(), 2)
        
        interview.completed = True
        interview.save()
        messages.success(request, "Assessment Complete!")
        return redirect("interview_result", interview_id=interview.id)

    return render(request, "resumes/ai_interview.html", {"questions": questions, "interview": interview})

@login_required
def interview_result(request, interview_id):
    interview = get_object_or_404(AIInterview, id=interview_id, candidate=request.user)
    return render(request, "resumes/interview_result.html", {
        "interview": interview,
        "questions": interview.questions.all()
    })

@login_required
def download_certificate(request, interview_id):
    interview = get_object_or_404(AIInterview, id=interview_id, candidate=request.user)
    if interview.total_score < 70:
        messages.error(request, "Score 70% or higher to earn a certificate.")
        return redirect('interview_result', interview_id=interview.id)

    return render(request, 'resumes/certificate_template.html', {
        'interview': interview,
        'candidate_name': request.user.get_full_name() or request.user.username,
        'date': interview.created_at.date()
    })

# --- 4. RECRUITER VIEWS ---

@login_required
def job_applicants_ranking(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job).select_related(
        'user', 'user__resume'
    ).order_by('-match_score')

    return render(request, 'recruiter/applicant_ranking.html', {
        'job': job,
        'applicants': applications
    })

@login_required
def update_application_status(request, app_id, status):
    """
    Handles recruiter decisions (Accept/Reject).
    """
    application = get_object_or_404(Application, id=app_id)
    new_status = status.upper()
    
    if new_status in ['ACCEPTED', 'REJECTED']:
        application.status = new_status
        application.save()
        messages.success(request, f"Application for {application.user.username} has been {new_status.lower()}.")
    
    return redirect('job_applicants_ranking', job_id=application.job.id)

# --- 5. API VIEWS ---
class MyResumeView(generics.RetrieveUpdateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        resume, _ = Resume.objects.get_or_create(user=self.request.user)
        return resume