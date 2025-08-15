from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import ContactForm
from courses.models import Video
from blog.models import Post
from shop.models import Product


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["latest_videos"] = Video.objects.all().order_by("-created_at")[:6]
        ctx["latest_products"] = Product.objects.filter(is_active=True).order_by("-created_at")[:6]
        ctx["latest_posts"] = Post.objects.all().order_by("-published_at")[:4]
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:contact")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# Create your views here.
