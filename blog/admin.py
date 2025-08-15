from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Post


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ("__str__", "published_at")
    search_fields = ("translations__title", "translations__content")


# Register your models here.
