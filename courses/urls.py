from django.urls import path
from .views import VideoListView, VideoDetailView

app_name = "videos"

urlpatterns = [
    path("", VideoListView.as_view(), name="list"),
    path("<slug:slug>/", VideoDetailView.as_view(), name="detail"),
]







