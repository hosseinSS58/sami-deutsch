from django.http import JsonResponse
from django.views.generic import ListView, View
from django.db.models import Q
from django.shortcuts import render
from courses.models import Video, VideoTag
from blog.models import Post, Category
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
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
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
                'duration_minutes': video.duration_minutes,
                'tags': list(video.tags.values_list('name', flat=True))
            })
        
        # جستجو در مقالات
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
        
        for post in posts:
            results.append({
                'type': 'posts',
                'title': post.title,
                'excerpt': post.content[:200] if post.content else '',
                'url': post.get_absolute_url(),
                'category': post.category.name if post.category else None,
                'created_at': post.published_at,
                'views_count': getattr(post, 'views_count', 0),
                'tags': [post.category.name] if post.category else []
            })
        
        # جستجو در محصولات
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
        
        for product in products:
            results.append({
                'type': 'products',
                'title': product.name,
                'excerpt': product.description,
                'url': product.get_absolute_url(),
                'category': 'محصول',
                'created_at': product.created_at,
                'views_count': 0,
                'tags': ['محصول آموزشی']
            })
        
        # جستجو در تگ‌های ویدیو
        video_tags = VideoTag.objects.filter(name__icontains=query)
        for tag in video_tags:
            videos_with_tag = tag.videos.all()[:3]  # حداکثر 3 ویدیو برای هر تگ
            for video in videos_with_tag:
                results.append({
                    'type': 'videos',
                    'title': f"{video.title} (تگ: {tag.name})",
                    'excerpt': f"ویدیو با تگ {tag.name}",
                    'url': video.get_absolute_url(),
                    'level': video.level,
                    'topic': video.get_topic_display(),
                    'created_at': video.created_at,
                    'views_count': getattr(video, 'views_count', 0),
                    'duration_minutes': video.duration_minutes,
                    'tags': [tag.name] + list(video.tags.exclude(id=tag.id).values_list('name', flat=True))
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
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).values_list('title', flat=True)[:3]
            suggestions.extend(video_titles)
            
            # پیشنهادات از مقالات
            post_titles = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).values_list('title', flat=True)[:3]
            suggestions.extend(post_titles)
            
            # پیشنهادات از محصولات
            product_names = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).values_list('name', flat=True)[:3]
            suggestions.extend(product_names)
            
            # پیشنهادات از تگ‌ها
            tag_names = VideoTag.objects.filter(name__icontains=query).values_list('name', flat=True)[:3]
            suggestions.extend(tag_names)
        
        # حذف موارد تکراری و محدود کردن به 10 مورد
        unique_suggestions = list(dict.fromkeys(suggestions))[:10]
        
        return JsonResponse({"suggestions": unique_suggestions})


# Create your views here.
