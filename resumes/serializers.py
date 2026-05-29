from rest_framework import serializers
from .models import Resume
from jobs.serializers import SkillSerializer

class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ["id", "file", "extracted_text", "skills", "uploaded_at"]
        read_only_fields = ["extracted_text", "skills", "uploaded_at"]
