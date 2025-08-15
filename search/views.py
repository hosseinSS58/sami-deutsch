from django.http import JsonResponse
from django.views.generic import ListView, View
from search.utils import get_meili_client, COURSE_INDEX, POST_INDEX, PRODUCT_INDEX


class SearchView(ListView):
    template_name = "search/results.html"
    context_object_name = "results"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return []
        client = get_meili_client()
        results = []
        for index, key in (
            (COURSE_INDEX, "title"),
            (POST_INDEX, "title"),
            (PRODUCT_INDEX, "name"),
        ):
            hits = client.index(index).search(query).get("hits", [])
            results.extend([h.get(key) for h in hits])
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "").strip()
        return context


class SuggestionView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        client = get_meili_client()
        suggestions = []
        if query:
            for index, key in (
                (COURSE_INDEX, "title"),
                (POST_INDEX, "title"),
                (PRODUCT_INDEX, "name"),
            ):
                hits = client.index(index).search(query, {"limit": 5}).get("hits", [])
                for h in hits:
                    val = h.get(key)
                    if val and val not in suggestions:
                        suggestions.append(val)
        return JsonResponse({"suggestions": suggestions[:10]})


# Create your views here.
