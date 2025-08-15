from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import get_language


class Post(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=250, verbose_name=_("عنوان")),
        slug=models.SlugField(max_length=270, unique=True, allow_unicode=True),
        content=models.TextField(verbose_name=_("محتوا")),
    )
    cover = models.ImageField(upload_to="blog/covers/", blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("مقاله")
        verbose_name_plural = _("مقالات")
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.safe_translation_getter("title", any_language=True) or f"Post {self.pk}"

    def get_absolute_url(self):
        from django.urls import reverse
        lang = get_language()
        slug_val = self.safe_translation_getter("slug", language_code=lang)
        if not slug_val:
            slug_val = self.safe_translation_getter("slug", any_language=True)
        return reverse("blog:detail", kwargs={"slug": slug_val})

    @property
    def slug_current(self) -> str:
        slug = self.safe_translation_getter("slug", language_code=getattr(self, "_current_language", None))
        if not slug:
            slug = self.safe_translation_getter("slug", any_language=True) or ""
        return slug


# Create your models here.
