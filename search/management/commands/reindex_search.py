from django.core.management.base import BaseCommand
from search.utils import get_meili_client, COURSE_INDEX, POST_INDEX, PRODUCT_INDEX
from courses.models import Course
from blog.models import Post
from shop.models import Product
from search.signals import serialize_course, serialize_post, serialize_product


class Command(BaseCommand):
    help = "Rebuild MeiliSearch indices for courses, posts, and products."

    def handle(self, *args, **options):
        client = get_meili_client()
        client.index(COURSE_INDEX).delete_all_documents()
        client.index(POST_INDEX).delete_all_documents()
        client.index(PRODUCT_INDEX).delete_all_documents()

        self.stdout.write("Indexing courses...")
        client.index(COURSE_INDEX).add_documents(
            [serialize_course(c) for c in Course.objects.all()], primary_key="id"
        )
        self.stdout.write("Indexing posts...")
        client.index(POST_INDEX).add_documents(
            [serialize_post(p) for p in Post.objects.all()], primary_key="id"
        )
        self.stdout.write("Indexing products...")
        client.index(PRODUCT_INDEX).add_documents(
            [serialize_product(p) for p in Product.objects.all()], primary_key="id"
        )
        self.stdout.write(self.style.SUCCESS("Reindex complete."))


