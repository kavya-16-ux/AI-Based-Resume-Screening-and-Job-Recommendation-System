from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Add this import

urlpatterns = [
    path("admin/", admin.site.urls),

    # Add these two lines for easy access
    path("login/", auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),

    # API Endpoints
    path("api/auth/", include("accounts.urls")),
    path("api/jobs/", include("jobs.urls")),
    path("api/resumes/", include("resumes.urls")),
    path("api/applications/", include("applications.urls")),

    # HTML Views & Authentication
    path("accounts/", include("accounts.urls")),
    path("", include("jobs.urls")), 
    path("resumes/", include("resumes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)