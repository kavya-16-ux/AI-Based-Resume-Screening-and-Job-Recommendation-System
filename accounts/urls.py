from django.urls import path
from django.contrib.auth import views as auth_views 
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, MeView, dashboard_redirect 

urlpatterns = [
    # 1. The Smart Redirect
    path("dashboard_redirect/", dashboard_redirect, name="dashboard-redirect"),

    # 2. HTML Authentication
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 3. Sign Up / Register
    # Use name="signup" here to match your current base.html
    path("signup/", SignupView.as_view(), name="signup"), 
    
    # 4. API Endpoints
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
]