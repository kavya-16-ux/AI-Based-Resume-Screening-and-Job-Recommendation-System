from django.urls import path
from . import views  # Import your views file

urlpatterns = [
    # The main HTML view for the "Apply Now" button
    path('apply/<int:job_id>/', views.apply_for_job, name='apply-job'),
    
    # List views for the dashboard
    path("mine/", views.MyApplicationsView.as_view(), name="my-applications"),
    path("job/<int:job_id>/", views.JobApplicationsView.as_view(), name="job-applications"),
]