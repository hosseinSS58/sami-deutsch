from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView,
    ProfileView,
    ProfileEditView,
    AdminDashboardView,
    AnalyticsDetailView,
    AnalyticsUserDetailView,
    AnalyticsAnonymousVisitorsView,
    AnalyticsAnonymousVisitorDetailView,
)
from .forms import CustomAuthForm

app_name = "accounts"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html", authentication_form=CustomAuthForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin/analytics/", AnalyticsDetailView.as_view(), name="analytics_detail"),
    path("admin/analytics/user/<int:user_id>/", AnalyticsUserDetailView.as_view(), name="analytics_user_detail"),
    path("admin/analytics/anonymous-visitors/", AnalyticsAnonymousVisitorsView.as_view(), name="analytics_anonymous_visitors"),
    path("admin/analytics/anonymous-visitor/<int:visitor_id>/", AnalyticsAnonymousVisitorDetailView.as_view(), name="analytics_anonymous_visitor_detail"),
    # Password reset views with security best practices
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="/accounts/password-reset/done/",
    ), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html",
    ), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url="/accounts/password-reset-complete/",
    ), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html",
    ), name="password_reset_complete"),
    # Password change (for logged-in users)
    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html",
        success_url="/accounts/password-change/done/",
    ), name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html",
    ), name="password_change_done"),
]





