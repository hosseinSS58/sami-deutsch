from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Q, Count
from .models import Video, VideoTag


class VideoListView(ListView):
    model = Video
    template_name = "videos/video_list.html"
    context_object_name = "videos"
    paginate_by = 12

    def get_queryset(self):
        queryset = Video.objects.all()
        
        # Filter by level
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by topic
        topic = self.request.GET.get('topic')
        if topic:
            queryset = queryset.filter(topic=topic)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by free/paid
        is_free = self.request.GET.get('is_free')
        if is_free == 'true':
            queryset = queryset.filter(is_free=True)
        elif is_free == 'false':
            queryset = queryset.filter(is_free=False)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.select_related().prefetch_related('tags', 'images', 'youtube_links')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter options
        context['levels'] = Video.objects.values_list('level', flat=True).distinct()
        context['topics'] = Video.objects.values_list('topic', flat=True).distinct()
        context['difficulties'] = Video.objects.values_list('difficulty', flat=True).distinct()
        context['tags'] = VideoTag.objects.annotate(video_count=Count('videos')).order_by('-video_count')[:20]
        
        # Add current filters
        context['current_filters'] = {
            'level': self.request.GET.get('level'),
            'topic': self.request.GET.get('topic'),
            'difficulty': self.request.GET.get('difficulty'),
            'is_free': self.request.GET.get('is_free'),
            'search': self.request.GET.get('search'),
        }
        
        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = "videos/video_detail.html"
    context_object_name = "video"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = Video.objects.filter(slug=slug).first()
        if not obj:
            raise Http404("Video not found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.object
        
        # Add related videos
        context['related_videos'] = Video.objects.filter(
            Q(level=video.level) | Q(topic=video.topic) | Q(tags__in=video.tags.all())
        ).exclude(pk=video.pk).distinct()[:6]
        
        # Add media counts
        context['total_images'] = video.images.filter(is_active=True).count()
        context['total_youtube'] = video.youtube_links.filter(is_active=True).count()
        
        return context


# Backward compatibility
CourseListView = VideoListView
CourseDetailView = VideoDetailView
