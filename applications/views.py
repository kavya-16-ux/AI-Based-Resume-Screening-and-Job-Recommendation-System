from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job
from resumes.models import Resume

@login_required
def apply_for_job(request, job_id):
    """HTML View: Handles the 'Apply Now' button from the Dashboard."""
    if request.method == "POST":
        job = get_object_or_404(Job, id=job_id)
        user = request.user
        
        # 1. Check if they have a resume (Required for your project logic)
        resume = Resume.objects.filter(user=user).first()
        if not resume:
            messages.error(request, "Please upload a resume before applying!")
            return redirect('upload-resume')

        # 2. Check for duplicate applications
        if Application.objects.filter(user=user, job=job).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect('candidate-dashboard')

        # 3. Capture the REAL AI data passed from the dashboard form
        score = request.POST.get('score', 0.0)
        missing = request.POST.getlist('missing_skills')

        # 4. Create the application with the actual BERT results
        Application.objects.create(
            user=user,
            job=job,
            resume=resume,
            match_score=float(score),
            missing_skills=missing
        )

        messages.success(request, f"Successfully applied for {job.title}!")
        return redirect('candidate-dashboard')

# Keep your existing API views for React/Postman support
class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).order_by("-applied_at")

class JobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Application.objects.filter(
            job_id=self.kwargs["job_id"], 
            job__recruiter=self.request.user
        ).order_by("-match_score")