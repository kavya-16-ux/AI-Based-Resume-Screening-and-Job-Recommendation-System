from rest_framework import serializers
from .models import Job, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]

class JobSerializer(serializers.ModelSerializer):
    # Keep your Skill object handling
    required_skills = SkillSerializer(many=True, read_only=True)
    skill_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    # Add the recruiter name for the API
    recruiter_username = serializers.CharField(source="recruiter.username", read_only=True)

    class Meta:
        model = Job
        # Updated to include NEW fields: company and location
        fields = [
            "id", "title", "company", "location", "description", 
            "required_skills", "skill_names", "recruiter_username", "created_at"
        ]
        # Recruiter is set automatically in the view, so it's read_only here
        read_only_fields = ["created_at", "recruiter"]

    def create(self, validated_data):
        skill_names = validated_data.pop("skill_names", [])
        job = Job.objects.create(**validated_data)
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name.strip().title())
            job.required_skills.add(skill)
        return job

    def update(self, instance, validated_data):
        skill_names = validated_data.pop("skill_names", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if skill_names is not None:
            instance.required_skills.clear()
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name.strip().title())
                instance.required_skills.add(skill)
        return instance