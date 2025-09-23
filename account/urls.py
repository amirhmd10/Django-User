from django.urls import path
from .views import LoginSignupView,ProfileUpdateView,UserSignUpView , UserLoginView,UserLogoutView


app_name = "account"

urlpatterns = [
    path("login", LoginSignupView.as_view(), name="login-signup"),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]
