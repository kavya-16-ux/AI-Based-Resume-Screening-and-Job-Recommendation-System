from django.urls import path
from . import views

urlpatterns = [
    # Candidate Routes
    path("dashboard/", views.candidate_dashboard, name="candidate-dashboard"),
    path("upload/", views.upload_resume_page, name="upload-resume"),
    
    # AI Interview Routes
    path("ai-interview/start/", views.start_ai_interview, name="start_ai_interview"),
    path("ai-interview/<int:interview_id>/", views.ai_interview, name="ai_interview"),
    path("ai-interview/<int:interview_id>/result/", views.interview_result, name="interview_result"),
    path("interview/<int:interview_id>/certificate/", views.download_certificate, name="download-certificate"),

    # Recruiter Routes
    path("job/<int:job_id>/ranking/", views.job_applicants_ranking, name="job_applicants_ranking"),
    
    # NEW: Application Status Decision Route (Accept/Reject)
    path("application/<int:app_id>/status/<str:status>/", views.update_application_status, name="update_status"),
]