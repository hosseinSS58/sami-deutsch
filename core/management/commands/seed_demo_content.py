from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.conf import settings

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import random

from blog.models import Post
from courses.models import Course
from shop.models import Product


class Command(BaseCommand):
    help = "Seed demo multilingual content for Posts, Courses, and Products (FA/EN/DE)."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding demo content..."))

        self._seed_posts()
        self._seed_courses()
        self._seed_products()

        # Ensure covers for any items without images
        self._ensure_covers()

        self.stdout.write(self.style.SUCCESS("Done seeding demo content."))

    # Posts
    def _seed_posts(self) -> None:
        posts = [
            {
                "fa": {
                    "title": "نکات طلایی یادگیری آلمانی",
                    "slug": "fa-german-learning-golden-tips",
                    "content": "در این مقاله چند نکته کلیدی برای شروع یادگیری زبان آلمانی را مرور می‌کنیم.",
                },
                "en": {
                    "title": "Golden Tips for Learning German",
                    "slug": "en-german-learning-golden-tips",
                    "content": "Key tips to kickstart your German learning journey.",
                },
                "de": {
                    "title": "Goldene Tipps zum Deutschlernen",
                    "slug": "de-goldene-tipps-zum-deutschlernen",
                    "content": "Wichtige Tipps für den Start beim Deutschlernen.",
                },
            },
            {
                "fa": {
                    "title": "گرامر ساده برای مبتدیان",
                    "slug": "fa-simple-grammar-for-beginners",
                    "content": "مروری سریع بر قواعد پایه آلمانی برای سطح A1.",
                },
                "en": {
                    "title": "Simple Grammar for Beginners",
                    "slug": "en-simple-grammar-for-beginners",
                    "content": "A quick overview of basic German grammar for A1 level.",
                },
                "de": {
                    "title": "Einfache Grammatik für Anfänger",
                    "slug": "de-einfache-grammatik-fur-anfanger",
                    "content": "Ein schneller Überblick über die deutsche Grundgrammatik für A1.",
                },
            },
            {
                "fa": {
                    "title": "واژگان پرکاربرد در سفر",
                    "slug": "fa-travel-vocabulary",
                    "content": "مهم‌ترین واژگان آلمانی که در سفر نیاز خواهید داشت.",
                },
                "en": {
                    "title": "Essential Travel Vocabulary",
                    "slug": "en-essential-travel-vocabulary",
                    "content": "Must-know German words for traveling.",
                },
                "de": {
                    "title": "Wichtiger Reisewortschatz",
                    "slug": "de-wichtiger-reisewortschatz",
                    "content": "Wichtige deutsche Wörter für Reisen.",
                },
            },
        ]

        created_count = 0
        for entry in posts:
            fa_slug = entry["fa"]["slug"]
            if Post.objects.filter(translations__language_code="fa", translations__slug=fa_slug).exists():
                continue
            post = Post()
            post.set_current_language("fa")
            post.title = entry["fa"]["title"]
            post.slug = fa_slug
            post.content = entry["fa"]["content"]
            post.save()
            # other translations
            for lang in ("en", "de"):
                post.create_translation(
                    language_code=lang,
                    title=entry[lang]["title"],
                    slug=entry[lang]["slug"],
                    content=entry[lang]["content"],
                )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Posts created: {created_count}"))

    # Courses
    def _seed_courses(self) -> None:
        courses = [
            {
                "level": "A1",
                "topic": "grammar",
                "fa": {"title": "دوره آلمانی A1 - شروع سریع", "slug": "fa-a1-fast-start", "description": "دوره مقدماتی A1"},
                "en": {"title": "German A1 - Fast Start", "slug": "en-a1-fast-start", "description": "Introductory A1 course"},
                "de": {"title": "Deutsch A1 - Schneller Start", "slug": "de-a1-schneller-start", "description": "Einführungskurs A1"},
            },
            {
                "level": "A2",
                "topic": "speaking",
                "fa": {"title": "مکالمه آلمانی A2", "slug": "fa-a2-speaking", "description": "تقویت مکالمه A2"},
                "en": {"title": "German Speaking A2", "slug": "en-a2-speaking", "description": "A2 speaking practice"},
                "de": {"title": "Deutsch Sprechen A2", "slug": "de-a2-sprechen", "description": "A2 Sprechübungen"},
            },
            {
                "level": "B1",
                "topic": "vocab",
                "fa": {"title": "واژگان آلمانی B1", "slug": "fa-b1-vocabulary", "description": "گسترش دایره لغات B1"},
                "en": {"title": "German Vocabulary B1", "slug": "en-b1-vocabulary", "description": "Expand your B1 vocabulary"},
                "de": {"title": "Deutscher Wortschatz B1", "slug": "de-b1-wortschatz", "description": "Wortschatz erweitern B1"},
            },
        ]

        created_count = 0
        for entry in courses:
            fa_slug = entry["fa"]["slug"]
            if Course.objects.filter(translations__language_code="fa", translations__slug=fa_slug).exists():
                continue
            course = Course(level=entry["level"], topic=entry["topic"])
            course.set_current_language("fa")
            course.title = entry["fa"]["title"]
            course.slug = fa_slug
            course.description = entry["fa"]["description"]
            course.save()
            for lang in ("en", "de"):
                course.create_translation(
                    language_code=lang,
                    title=entry[lang]["title"],
                    slug=entry[lang]["slug"],
                    description=entry[lang]["description"],
                )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Courses created: {created_count}"))

    # Products
    def _seed_products(self) -> None:
        products = [
            {
                "price": 350000,
                "fa": {"name": "پکیج شروع آلمانی A1", "slug": "fa-a1-starter-pack", "description": "پکیج شروع سریع سطح A1"},
                "en": {"name": "A1 German Starter Pack", "slug": "en-a1-starter-pack", "description": "Fast start A1 pack"},
                "de": {"name": "A1 Deutsch Starterpaket", "slug": "de-a1-starterpaket", "description": "Schnellstart-Paket A1"},
            },
            {
                "price": 540000,
                "fa": {"name": "پکیج جامع A2", "slug": "fa-a2-complete-pack", "description": "پکیج کامل سطح A2"},
                "en": {"name": "A2 Complete Pack", "slug": "en-a2-complete-pack", "description": "Complete A2 pack"},
                "de": {"name": "A2 Komplettpaket", "slug": "de-a2-komplettpaket", "description": "Komplettpaket A2"},
            },
            {
                "price": 790000,
                "fa": {"name": "پکیج واژگان B1", "slug": "fa-b1-vocab-pack", "description": "واژگان ضروری B1"},
                "en": {"name": "B1 Vocabulary Pack", "slug": "en-b1-vocab-pack", "description": "Essential B1 vocabulary"},
                "de": {"name": "B1 Wortschatzpaket", "slug": "de-b1-wortschatzpaket", "description": "Wichtiger Wortschatz B1"},
            },
        ]

        created_count = 0
        for entry in products:
            fa_slug = entry["fa"]["slug"]
            if Product.objects.filter(translations__language_code="fa", translations__slug=fa_slug).exists():
                continue
            product = Product(price=entry["price"], is_active=True)
            product.set_current_language("fa")
            product.name = entry["fa"]["name"]
            product.slug = fa_slug
            product.description = entry["fa"]["description"]
            product.save()
            for lang in ("en", "de"):
                product.create_translation(
                    language_code=lang,
                    name=entry[lang]["name"],
                    slug=entry[lang]["slug"],
                    description=entry[lang]["description"],
                )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Products created: {created_count}"))

    def _ensure_covers(self) -> None:
        os.makedirs(getattr(settings, "MEDIA_ROOT", "media"), exist_ok=True)

        def generate_cover(text: str, bg: tuple[int, int, int] | None = None) -> ContentFile:
            width, height = 1200, 675
            if bg is None:
                # pleasant blue range
                bg = random.choice([(25, 118, 210), (30, 136, 229), (21, 101, 192), (2, 119, 189)])
            img = Image.new("RGB", (width, height), color=bg)
            draw = ImageDraw.Draw(img)
            # try to load a common font; fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 56)
            except Exception:
                font = ImageFont.load_default()
            text = (text or "SAMI").strip()[:40]
            tw, th = draw.textbbox((0, 0), text, font=font)[2:]
            x = (width - tw) // 2
            y = (height - th) // 2
            # semi-transparent overlay band for readability
            band_height = th + 60
            band_top = max(0, y - 30)
            band = Image.new("RGBA", (width, band_height), color=(0, 0, 0, 90))
            img.paste(band, (0, band_top), band)
            draw = ImageDraw.Draw(img)
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=88)
            return ContentFile(buf.getvalue())

        # Posts
        for p in Post.objects.all():
            if not p.cover:
                filename = f"blog_{p.pk}.jpg"
                content = generate_cover(p.safe_translation_getter("title", any_language=True) or "Blog")
                p.cover.save(filename, content, save=True)

        # Courses
        for c in Course.objects.all():
            if not c.cover:
                filename = f"course_{c.pk}.jpg"
                content = generate_cover(c.safe_translation_getter("title", any_language=True) or "Course")
                c.cover.save(filename, content, save=True)

        # Products
        for pr in Product.objects.all():
            if not pr.cover:
                filename = f"product_{pr.pk}.jpg"
                content = generate_cover(pr.safe_translation_getter("name", any_language=True) or "Product")
                pr.cover.save(filename, content, save=True)


