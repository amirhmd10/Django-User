from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserSignUpForm, UserLoginForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView



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




