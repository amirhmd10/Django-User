import code
import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import FormView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserSignUpForm, UserLoginForm, ProfileForm, EmailForm, OTPForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from .models import EmailOTP , PasswordReset



User = get_user_model()

class LoginSignupView(TemplateView):
    template_name = "account/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_form'] = UserSignUpForm()
        context['login_form'] = UserLoginForm()
        return context


class UserSignUpView(FormView):
    template_name = "account/index.html"
    form_class = UserSignUpForm
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created. You may now login.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong.")
        return redirect("account:login")


class UserLoginView(FormView):
    template_name = "account/index.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "You are now logged in.")
            return super().form_valid(form)
        messages.error(self.request, "You are not logged in.")
        return redirect("account:profile")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("account:login")



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    success_url = reverse_lazy("account:profile")

    def get_object(self, queryset=None):
        return self.request.user


class RequestOTPView(FormView):
    template_name = "account/index.html"
    form_class = EmailForm
    success_url = '/verify/'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        code = f"{secrets.randbelow(9000) + 1000}"
        # code = "{:04d}".format(secrets.randbelow(10000))

        EmailOTP.objects.create(email=email, code=code)
        send_mail(
            subject="OTP Requested",
            message= f'your code is {code}',
            from_email= '<EMAIL>',
            recipient_list=[email],
        )
        return super().form_valid(form)


MAX_ATTEMPTS = 10
BLOCKED_TIME = 10


class VerifyEmailView(FormView):
    template_name = "account/index.html"
    form_class = OTPForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        code = form.cleaned_data.get("code")
        try :
            otp = EmailOTP.objects.filter(email=email, code=code , is_used=False).latest('created_at')
        except EmailOTP.DoesNotExist:
            form.add_error(None , 'invalid code')
            return self.form_invalid(form)

        if otp.is_blocked:
            remaining = (otp.is_blocked - timezone.now() ). seconds // 60+1
            form.add_error(None , 'too many attempts . try after 10 minutes ')
            return self.form_invalid(form)


        if otp.is_expired():
            form.add_error(None , 'expired')
            return self.form_invalid(form)



        if otp.attempts >= MAX_ATTEMPTS:
            form.add_error(None , 'too many attempts')
            return self.form_invalid(form)
        otp.attempts +=1
        otp.save(update_fields=['attempted'])


        otp.is_used = True
        otp.attempts = 0
        otp.save(update_fields=['is_used' , 'attempts'])

        user, created = User.objects.get_or_create(email=email)

        if created:
            user.set_unusable_password()


        user.is_active = True
        user.save()


        login(self.request, user)
        return redirect( self.get_success_url() )



class PasswordResetRequestView (FormView):
    template_name = "account/index.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("account:login")
    
    
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        try :
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_valid(form)
        
        token = PasswordReset.objects.create(user=user)
        
        reset_url = self.request.build_absolute_uri(
            reverse('account:password_reset_confirm', kwargs={'token': str(token.token)})
        )
        send_mail(
            subject="Password Reset",
            message= f'your code is {code}',
            from_email= settings.Default_FROM_EMAIL,
            recipient_list=[email],
        )
        return super().form_valid(form)


class PasswordResetConfirmView (FormView):
    template_name = "account/index.html"
    form_class = EmailForm
    success_url = reverse_lazy("account:login")

    def dispatch(self, request, *args, **kwargs):
        self.token = get_object_or_404(PasswordReset, token=kwargs['token'] , is_used=False)
        if self.token.is_expired():
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        password = form.cleaned_data.get("password1")
        user = self.token.user
        user.set_password(password)
        user.save()


        self.token.is_used = True
        self.token.save()
        return super().form_valid(form)



