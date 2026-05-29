from django.db import models
from django.conf import settings
from jobs.models import Skill

class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume")
    file = models.FileField(upload_to="resumes/")
    extracted_text = models.TextField(blank=True, default="")
    skills = models.ManyToManyField(Skill, related_name="resumes", blank=True)
    extracted_skills = models.JSONField(default=list, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume of {self.user.username}"

class AIInterview(models.Model):
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    missing_skills = models.TextField()  
    total_score = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview: {self.candidate.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class InterviewQuestion(models.Model):
    interview = models.ForeignKey(AIInterview, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    ideal_answer = models.TextField(blank=True, null=True)
    candidate_answer = models.TextField(blank=True, null=True)
    score = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.question[:50]