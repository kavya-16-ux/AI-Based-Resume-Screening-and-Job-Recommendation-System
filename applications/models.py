from django.db import models
from django.conf import settings
from jobs.models import Job
from resumes.models import Resume

class Application(models.Model):
    # Status Options
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    # Links
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="applications",
        null=True,
        blank=True
    )

    # AI Data
    match_score = models.FloatField(default=0.0)
    missing_skills = models.JSONField(blank=True, default=list)
    
    # Metadata & Recruiter Decision
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )

    class Meta:
        # Prevents a candidate from applying to the same job twice
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} -> {self.job.title} ({self.status})"