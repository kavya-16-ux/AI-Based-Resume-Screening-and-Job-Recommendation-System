from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    SignupSerializer, 
    LoginSerializer, 
    UserSerializer, 
    get_tokens_for_user
)

# 1. Signup View (Direct Flow)
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Display the HTML signup form directly."""
        return render(request, "accounts/signup.html")

    def create(self, request, *args, **kwargs):
        """Process registration and redirect immediately to dashboard."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log the user in immediately so they are authenticated for the dashboard
        login(request, user)

        # Detect if the request is from a browser
        is_browser = (
            request.accepted_renderer.format == 'html' or 
            'text/html' in request.headers.get('Accept', '')
        )

        if is_browser:
            return redirect('dashboard-redirect')

        # Fallback for API/Postman
        return Response({
            "user": UserSerializer(user).data,
            "tokens": get_tokens_for_user(user),
        }, status=status.HTTP_201_CREATED)


# 2. Login View (Direct Flow)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Display the HTML login page."""
        return render(request, "accounts/login.html")

    def post(self, request):
        """Handle login and redirect browser users directly."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Log the user into the session
        login(request, user)

        # Detect if the request is from a browser
        is_browser = (
            request.accepted_renderer.format == 'html' or 
            'text/html' in request.headers.get('Accept', '')
        )

        if is_browser:
            return redirect('dashboard-redirect')

        # Otherwise, return JSON tokens
        return Response({
            "user": UserSerializer(user).data,
            "tokens": get_tokens_for_user(user),
        })


# 3. Me View (API Only)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)


# 4. Smart Redirect View (Traffic Controller)
@login_required
def dashboard_redirect(request):
    """Redirects users to their specific dashboard based on their role."""
    # Ensure user has a role attribute before checking
    role = getattr(request.user, 'role', None)
    
    if role == "RECRUITER":
        return redirect('recruiter-dashboard')
    elif role == "CANDIDATE":
        return redirect('candidate-dashboard')
    
    # Fallback for admins or users without roles
    return redirect('/admin/')