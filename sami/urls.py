"""
URL configuration for sami project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, CourseSitemap, PostSitemap, ProductSitemap

# Admin site customization
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),

    path("sitemap.xml", sitemap, {"sitemaps": {
        "static": StaticViewSitemap,
        "courses": CourseSitemap,
        "blog": PostSitemap,
        "shop": ProductSitemap,
    }}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("core.urls")),
    path("videos/", include("courses.urls")),  # Videos use the same views as courses
    path("blog/", include("blog.urls")),
    path("shop/", include("shop.urls")),
    path("accounts/", include("accounts.urls")),
    path("search/", include("search.urls")),
    path("assessments/", include("assessments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
