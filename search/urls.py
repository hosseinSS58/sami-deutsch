from django.urls import path
from .views import SearchView, SuggestionView

app_name = "search"

urlpatterns = [
    path("", SearchView.as_view(), name="search"),
    path("suggest/", SuggestionView.as_view(), name="suggest"),
]







