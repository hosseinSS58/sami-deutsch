from django.test import TestCase
from django.urls import reverse

from shop.models import Order
from tests.factories import create_product


class ShopFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = create_product(name="Complete Pack", price=250000)

    def test_product_list_view(self):
        response = self.client.get(reverse("shop:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Complete Pack")

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Complete Pack")

    def test_add_to_cart_stores_session(self):
        response = self.client.post(
            reverse("shop:add_to_cart"),
            {"product_id": self.product.id, "quantity": 2},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        cart = self.client.session.get("cart", {})
        self.assertEqual(cart.get(str(self.product.id)), 2)

    def test_checkout_creates_order_and_clears_cart(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): 2}
        session.save()
        payload = {
            "full_name": "Hossein G.",
            "email": "buyer@example.com",
            "phone": "09120000000",
            "address": "Tehran",
        }
        response = self.client.post(reverse("shop:checkout"), payload)
        order = Order.objects.latest("id")
        self.assertRedirects(response, reverse("shop:success", kwargs={"order_id": order.id}))
        self.assertEqual(order.total_amount, self.product.price * 2)
        self.assertEqual(self.client.session.get("cart"), {})
