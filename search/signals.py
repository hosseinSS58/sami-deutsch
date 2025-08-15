from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils import get_meili_client, COURSE_INDEX, POST_INDEX, PRODUCT_INDEX
from courses.models import Course
from blog.models import Post
from shop.models import Product
import logging

logger = logging.getLogger(__name__)


def serialize_course(obj: Course) -> dict:
    return {
        "id": obj.id,
        "title": obj.safe_translation_getter("title", any_language=True),
        "description": obj.safe_translation_getter("description", any_language=True),
        "slug": obj.safe_translation_getter("slug", any_language=True),
        "level": obj.level,
        "topic": obj.topic,
    }


def serialize_post(obj: Post) -> dict:
    return {
        "id": obj.id,
        "title": obj.safe_translation_getter("title", any_language=True),
        "content": obj.safe_translation_getter("content", any_language=True),
        "slug": obj.safe_translation_getter("slug", any_language=True),
    }


def serialize_product(obj: Product) -> dict:
    return {
        "id": obj.id,
        "name": obj.safe_translation_getter("name", any_language=True),
        "description": obj.safe_translation_getter("description", any_language=True),
        "slug": obj.safe_translation_getter("slug", any_language=True),
        "price": obj.price,
        "is_active": obj.is_active,
    }


def upsert(index: str, payload: dict):
    try:
        client = get_meili_client()
        client.index(index).add_documents([payload], primary_key="id")
    except Exception as exc:
        logger.warning("Search upsert skipped (%s): %s", index, exc)


def remove(index: str, object_id: int):
    try:
        client = get_meili_client()
        client.index(index).delete_document(object_id)
    except Exception as exc:
        logger.warning("Search remove skipped (%s): %s", index, exc)


@receiver(post_save, sender=Course)
def course_saved(sender, instance: Course, **kwargs):
    upsert(COURSE_INDEX, serialize_course(instance))


@receiver(post_delete, sender=Course)
def course_deleted(sender, instance: Course, **kwargs):
    remove(COURSE_INDEX, instance.id)


@receiver(post_save, sender=Post)
def post_saved(sender, instance: Post, **kwargs):
    upsert(POST_INDEX, serialize_post(instance))


@receiver(post_delete, sender=Post)
def post_deleted(sender, instance: Post, **kwargs):
    remove(POST_INDEX, instance.id)


@receiver(post_save, sender=Product)
def product_saved(sender, instance: Product, **kwargs):
    upsert(PRODUCT_INDEX, serialize_product(instance))


@receiver(post_delete, sender=Product)
def product_deleted(sender, instance: Product, **kwargs):
    remove(PRODUCT_INDEX, instance.id)


