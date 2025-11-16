import uuid
from typing import Tuple

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Profile
from assessments.models import Assessment, Question, Choice
from blog.models import Category, Post
from courses.models import Video
from shop.models import Product, Order, OrderItem
from siteconfig.models import SiteSettings


def _unique_slug(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_user(username: str = "user", email: str | None = None, password: str = "Testpass123!") -> Tuple:
    """Create and return a user and its password."""
    user_model = get_user_model()
    email_value = email or f"{username}@example.com"
    user, created = user_model.objects.get_or_create(
        username=username,
        defaults={
            "email": email_value,
            "first_name": "Test",
            "last_name": "User",
        },
    )
    if created or not user.check_password(password):
        user.set_password(password)
        user.save()
    Profile.objects.get_or_create(user=user)
    return user, password


def create_category(name: str = "Grammar") -> Category:
    return Category.objects.create(name=name, slug=_unique_slug("category"))


def create_post(title: str = "Sample Post", category: Category | None = None) -> Post:
    category = category or create_category()
    return Post.objects.create(
        title=title,
        slug=_unique_slug("post"),
        content="Sample content for testing.",
        category=category,
    )


def create_video(title: str = "Sample Video", level: str = "A1") -> Video:
    return Video.objects.create(
        title=title,
        slug=_unique_slug("video"),
        description="Video description",
        level=level,
        topic="grammar",
        duration_minutes=15,
        difficulty="beginner",
        is_featured=True,
    )


def create_product(name: str = "Starter Kit", price: int = 100000) -> Product:
    return Product.objects.create(
        name=name,
        slug=_unique_slug("product"),
        description="Product description for testing.",
        price=price,
        is_active=True,
    )


def create_order_with_item(product: Product | None = None, quantity: int = 1) -> Order:
    product = product or create_product()
    order = Order.objects.create(
        full_name="Test Buyer",
        email="buyer@example.com",
        phone="1234567890",
        address="Street 1",
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        unit_price=product.price,
        line_total=product.price * quantity,
    )
    order.recalculate_total()
    return order


def ensure_site_settings() -> SiteSettings:
    return SiteSettings.load()


def create_assessment_with_question() -> tuple[Assessment, Question, Choice]:
    assessment = Assessment.objects.create(
        title="Placement Test",
        level="A1",
        is_active=True,
        time_limit_seconds=600,
        attempt_limit=3,
    )
    question = Question.objects.create(
        assessment=assessment,
        text="Select the correct option",
        type=Question.QuestionType.MCQ_SINGLE,
        target_level="A1",
        difficulty=Question.Difficulty.EASY,
        weight=2,
    )
    correct_choice = Choice.objects.create(question=question, text="Correct", is_correct=True)
    Choice.objects.create(question=question, text="Incorrect", is_correct=False)
    return assessment, question, correct_choice



