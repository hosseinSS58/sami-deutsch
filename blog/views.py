from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Post.objects.all().select_related("category")
        
        # Search functionality
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            ).distinct()
        
        # Category filter
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Featured filter
        featured = self.request.GET.get("featured")
        if featured == "true":
            queryset = queryset.filter(is_featured=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_category"] = self.request.GET.get("category")
        context["selected_featured"] = self.request.GET.get("featured")
        context["total_posts"] = self.get_queryset().count()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = Post.objects.filter(slug=slug).select_related("category").first()
        if not obj:
            raise Http404(_("مقاله یافت نشد"))
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Increment view count
        self.object.increment_views()
        
        # Get related posts
        related_posts = Post.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        
        context["related_posts"] = related_posts
        context["categories"] = Category.objects.all()
        return context


# Create your views here.
