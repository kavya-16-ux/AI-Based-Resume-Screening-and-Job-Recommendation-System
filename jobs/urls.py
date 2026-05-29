from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Setup the API Router (Automates List, Create, Retrieve, Update, Delete)
router = DefaultRouter()
router.register(r"api/jobs", views.JobViewSet, basename="job-api")

urlpatterns = [
    # --- HTML DASHBOARD (WEB INTERFACE) ---
    path("recruiter/jobs/", views.recruiter_dashboard), # Fallback URL
    path("recruiter/dashboard/", views.recruiter_dashboard, name="recruiter-dashboard"),
    
    # CRUD Operations for Web UI
    path("recruiter/jobs/create/", views.job_create, name="job-create"),
    path("recruiter/jobs/<int:job_id>/edit/", views.job_update, name="job-update"),
    path("recruiter/jobs/<int:job_id>/delete/", views.job_delete, name="job-delete"),
    
    # AI Ranking Page for Web UI
    path("recruiter/jobs/<int:job_id>/applicants/", views.job_applicants, name="job-applicants"),

    # --- GENERIC API ENDPOINTS (FOR REACT/FRONTEND) ---
    # List and Create jobs via JSON
    path("api/recruiter/jobs/", views.RecruiterJobListCreateAPIView.as_view(), name="api-recruiter-jobs"),
    
    # Individual job detail (Retrieve, Update, Destroy) via JSON
    path("api/recruiter/jobs/<int:pk>/", views.RecruiterJobDetailAPIView.as_view(), name="api-recruiter-job-detail"),
    
    # Get ranked applicants for a job via JSON
    path("api/recruiter/jobs/<int:job_id>/applicants/", views.RecruiterJobApplicantsAPIView.as_view(), name="api-recruiter-job-applicants"),

    # --- ROUTER API ---
    path("", include(router.urls)),
]