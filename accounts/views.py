from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import SignUpForm, CustomAuthForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["avatar", "phone", "level", "bio", "website", "newsletter_opt_in"]
    template_name = "accounts/profile_edit.html"

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy("accounts:profile")


# Create your views here.
