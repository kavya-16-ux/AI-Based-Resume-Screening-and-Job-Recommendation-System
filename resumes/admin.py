from django.contrib import admin
from .models import Resume, AIInterview, InterviewQuestion

admin.site.register(Resume)
admin.site.register(AIInterview)
admin.site.register(InterviewQuestion)