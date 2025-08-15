from django.http import JsonResponse
from django.views.generic import ListView, View
from django.db.models import Q
from django.shortcuts import render
from courses.models import Video
from blog.models import Post
from shop.models import Product


class SearchView(ListView):
    template_name = "search/results.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return []
        
        results = []
        
        # جستجو در ویدیوها
        videos = Video.objects.filter(
            Q(translations__title__icontains=query) |
            Q(translations__description__icontains=query)
        ).distinct()
        
        for video in videos:
            results.append({
                'type': 'videos',
                'title': video.title,
                'excerpt': video.description,
                'url': video.get_absolute_url(),
                'level': video.level,
                'topic': video.get_topic_display(),
                'created_at': video.created_at,
                'views_count': getattr(video, 'views_count', 0),
                'duration_minutes': video.duration_minutes
            })
        
        # جستجو در مقالات
        posts = Post.objects.filter(
            Q(translations__title__icontains=query) |
            Q(translations__content__icontains=query)
        ).distinct()
        
        for post in posts:
            results.append({
                'type': 'posts',
                'title': post.title,
                'excerpt': post.content[:200] if post.content else '',
                'url': post.get_absolute_url(),
                'category': post.category.name if post.category else None,
                'created_at': post.published_at,
                'views_count': getattr(post, 'views_count', 0)
            })
        
        # جستجو در محصولات
        products = Product.objects.filter(
            Q(translations__name__icontains=query) |
            Q(translations__description__icontains=query)
        ).distinct()
        
        for product in products:
            results.append({
                'type': 'products',
                'title': product.name,
                'excerpt': product.description,
                'url': product.get_absolute_url(),
                'category': product.category.name if product.category else None,
                'created_at': product.created_at,
                'views_count': getattr(product, 'views_count', 0)
            })
        
        # مرتب‌سازی بر اساس تاریخ
        results.sort(key=lambda x: x['created_at'], reverse=True)
        
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        context["total_results"] = len(self.get_queryset())
        return context


class SuggestionView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        suggestions = []
        
        if query:
            # پیشنهادات از ویدیوها
            video_titles = Video.objects.filter(
                translations__title__icontains=query
            ).values_list('translations__title', flat=True)[:3]
            suggestions.extend(video_titles)
            
            # پیشنهادات از مقالات
            post_titles = Post.objects.filter(
                translations__title__icontains=query
            ).values_list('translations__title', flat=True)[:3]
            suggestions.extend(post_titles)
            
            # پیشنهادات از محصولات
            product_names = Product.objects.filter(
                translations__name__icontains=query
            ).values_list('translations__name', flat=True)[:3]
            suggestions.extend(product_names)
        
        # حذف موارد تکراری و محدود کردن به 10 مورد
        unique_suggestions = list(dict.fromkeys(suggestions))[:10]
        
        return JsonResponse({"suggestions": unique_suggestions})


# Create your views here.
