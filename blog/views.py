from django.views.generic import ListView, DetailView
from django.http import Http404
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        lang = getattr(self.request, "LANGUAGE_CODE", None)
        qs = Post.objects.all()
        if lang:
            obj = qs.filter(translations__language_code=lang, translations__slug=slug).first()
            if obj:
                return obj
        obj = qs.filter(translations__slug=slug).first()
        if obj:
            return obj
        raise Http404("Post not found")


# Create your views here.
