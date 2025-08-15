from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from courses.models import Course
from blog.models import Post
from shop.models import Product


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["core:home", "core:about", "core:contact", "courses:list", "blog:list", "shop:list"]

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Course.objects.all()


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.all()


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Product.objects.filter(is_active=True)







