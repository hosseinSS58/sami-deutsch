from django.conf import settings
from meilisearch import Client


def get_meili_client() -> Client:
    return Client(settings.MEILI_URL, settings.MEILI_API_KEY)


COURSE_INDEX = "courses"
POST_INDEX = "posts"
PRODUCT_INDEX = "products"







