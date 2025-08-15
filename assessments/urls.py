from django.urls import path
from .views import AssessmentIntroView, AssessmentTakeView, AssessmentResultView

app_name = "assessments"

urlpatterns = [
    path("", AssessmentIntroView.as_view(), name="intro"),
    path("take/", AssessmentTakeView.as_view(), name="take"),
    path("result/", AssessmentResultView.as_view(), name="result"),
]







