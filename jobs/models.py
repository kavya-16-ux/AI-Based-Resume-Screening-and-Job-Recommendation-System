from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    # Added 'related_name="posted_jobs"' to match the Step 4 instructions
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs")
    title = models.CharField(max_length=200)
    
    # NEW FIELDS NEEDED FOR THE DASHBOARD:
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    description = models.TextField()
    
    # KEEPING YOUR SKILL MODEL (More professional)
    required_skills = models.ManyToManyField(Skill, related_name="jobs", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title