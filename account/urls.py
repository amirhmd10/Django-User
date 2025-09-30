from django.urls import path
from .views import (
    LoginSignupView,
    UserSignUpView,
    UserLoginView,
    UserLogoutView,
    ProfileUpdateView,
    RequestOTPView,
    VerifyEmailView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

app_name = "account"

urlpatterns = [
    path("", LoginSignupView.as_view(), name="login"),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login_user"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("request-otp/", RequestOTPView.as_view(), name="request_otp"),
    path("verify/", VerifyEmailView.as_view(), name="verify_email"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/<uuid:token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
