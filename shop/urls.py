from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CartView,
    AddToCartView,
    RemoveFromCartView,
    CheckoutView,
    CheckoutSuccessView,
)

app_name = "shop"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/remove/", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("success/<int:order_id>/", CheckoutSuccessView.as_view(), name="success"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]


