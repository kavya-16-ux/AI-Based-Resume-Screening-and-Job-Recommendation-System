from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "user",
            "username",
            "job",
            "job_title",
            "resume",            # NEW — needed for ML
            "match_score",
            "missing_skills",    # NEW — ML output
            "applied_at",
        ]
        read_only_fields = [
            "user",
            "match_score",
            "missing_skills",    # NEW — set by ML, not user
            "applied_at",
        ]
