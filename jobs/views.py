from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, generics

# Import models, forms, and serializers
from .models import Job
from .forms import JobForm
from .serializers import JobSerializer
from applications.models import Application
from applications.serializers import ApplicationSerializer

# --- 1. PERMISSIONS ---
class IsRecruiterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and getattr(request.user, 'role', None) == "RECRUITER"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.recruiter == request.user

# --- 2. API VIEWS (REST Framework) ---

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class RecruiterJobListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class RecruiterJobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

class RecruiterJobApplicantsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return Application.objects.filter(
            job_id=job_id,
            job__recruiter=self.request.user
        ).order_by("-match_score")


# --- 3. CANDIDATE ACTION VIEWS ---

@login_required
def apply_job(request, job_id):
    """
    Handles the POST request from the candidate dashboard to apply for a job.
    Saves BERT match scores and missing skills.
    """
    if request.method == "POST":
        job = get_object_or_404(Job, id=job_id)
        
        # Extract data from hidden form fields
        score = request.POST.get('score', 0.0)
        m_skills = request.POST.getlist('missing_skills')

        # Prevent duplicate applications
        application, created = Application.objects.get_or_create(
            user=request.user,
            job=job,
            defaults={
                'match_score': score,
                'missing_skills': m_skills,
                'status': 'PENDING'
            }
        )

        if created:
            messages.success(request, f"Successfully applied for {job.title}!")
        else:
            messages.info(request, "You have already applied for this job.")

        return redirect('candidate-dashboard')
    
    return redirect('candidate-dashboard')


# --- 4. RECRUITER TEMPLATE VIEWS ---

@login_required
def recruiter_dashboard(request):
    jobs = Job.objects.filter(recruiter=request.user).order_by("-created_at")
    total_jobs = jobs.count()
    total_applicants = Application.objects.filter(job__recruiter=request.user).count()
    
    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,
        "total_applicants": total_applicants,
    }
    return render(request, "jobs/recruiter_dashboard.html", context)

@login_required
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            form.save_m2m() 
            messages.success(request, "Job created successfully.")
            return redirect("recruiter-dashboard")
    else:
        form = JobForm()
    
    return render(request, "jobs/job_form.html", {
        "form": form,
        "title": "Create Job",
        "button_text": "Create Job",
    })

@login_required
def job_update(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect("recruiter-dashboard")
    else:
        form = JobForm(instance=job)
    
    return render(request, "jobs/job_form.html", {
        "form": form,
        "title": "Update Job",
        "button_text": "Update Job",
    })

@login_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("recruiter-dashboard")
    return render(request, "jobs/job_confirm_delete.html", {"job": job})

@login_required
def job_applicants(request, job_id):
    # Check if the job exists at all first
    job = get_object_or_404(Job, id=job_id)
    
    # Check if the current user is the recruiter who posted it
    # OR if they are a superuser (for easier demoing)
    if job.recruiter != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to view these applicants.")
        return redirect('recruiter-dashboard')

    # Get the applications
    applications = Application.objects.filter(job=job).select_related(
        "user", "job"
    ).order_by("-match_score")
    
    ranked_applications = []
    for index, application in enumerate(applications, start=1):
        ranked_applications.append({
            "rank": index,
            "application": application,
        })
    
    context = {
        "job": job,
        "applicants": applications, # Use 'applicants' to match your ranking template
        "ranked_applications": ranked_applications,
    }
    return render(request, "recruiter/applicant_ranking.html", context)