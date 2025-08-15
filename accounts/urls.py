from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, ProfileView, ProfileEditView
from .forms import CustomAuthForm

app_name = "accounts"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html", authentication_form=CustomAuthForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]





