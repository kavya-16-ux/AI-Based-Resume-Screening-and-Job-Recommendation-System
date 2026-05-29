from django import forms
from .models import Job, Skill

class JobForm(forms.ModelForm):
    # This field acts as the bridge: UI (Text) -> Logic (Objects)
    skills_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Example: Python, Django, REST API, SQL"
        }),
        label="Required Skills"
    )

    class Meta:
        model = Job
        fields = [
            "title",
            "company",
            "location",
            "description",
            "skills_text",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing, convert Skill objects back into a comma-separated string
        if self.instance and self.instance.pk:
            self.fields["skills_text"].initial = ", ".join(
                [s.name for s in self.instance.required_skills.all()]
            )

    def save(self, commit=True):
        # 1. Save the basic job data (Title, Description, etc.)
        job = super().save(commit=False)
        
        if commit:
            job.save()

        # 2. Process the text into individual Skill objects
        skills_raw = self.cleaned_data.get("skills_text", "")
        skill_names = [s.strip().title() for s in skills_raw.split(",") if s.strip()]

        skill_objects = []
        for name in skill_names:
            # This ensures we don't create duplicate skills in the database
            skill, created = Skill.objects.get_or_create(name=name)
            skill_objects.append(skill)

        # 3. Use .set() to update the ManyToMany relationship
        if commit:
            job.required_skills.set(skill_objects)
        else:
            # Setup save_m2m for views that use commit=False
            def save_m2m():
                job.required_skills.set(skill_objects)
            self.save_m2m = save_m2m

        return job