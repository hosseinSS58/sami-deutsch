from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View, FormView
from django.http import Http404
from django.contrib import messages
from .models import Product, Order, OrderItem
from .forms import AddToCartForm, CheckoutForm


class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = Product.objects.filter(slug=slug, is_active=True).first()
        if not obj:
            raise Http404("Product not found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddToCartForm(initial={"product_id": self.object.id})
        return context


class CartView(TemplateView):
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})
        items = []
        total = 0
        for product_id, qty in cart.items():
            product = Product.objects.filter(id=product_id).first()
            if not product:
                continue
            unit_price = product.price
            line_total = unit_price * qty
            total += line_total
            items.append({
                "product": product,
                "quantity": qty,
                "unit_price": unit_price,
                "line_total": line_total,
            })
        context.update({"items": items, "total": total})
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, id=form.cleaned_data["product_id"])
            qty = form.cleaned_data.get("quantity", 1)
            cart = request.session.get("cart", {})
            cart[str(product.id)] = cart.get(str(product.id), 0) + qty
            request.session["cart"] = cart
        return redirect("shop:cart")


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        try:
            product_id = int(request.POST.get("product_id"))
        except (ValueError, TypeError):
            messages.error(request, "Invalid product ID")
            return redirect("shop:cart")
        
        # بررسی وجود product
        if not Product.objects.filter(id=product_id, is_active=True).exists():
            messages.error(request, "Product not found")
            return redirect("shop:cart")
        
        cart = request.session.get("cart", {})
        if str(product_id) in cart:
            cart.pop(str(product_id))
            request.session["cart"] = cart
            messages.success(request, "Product removed from cart")
        
        return redirect("shop:cart")


class CheckoutView(FormView):
    template_name = "shop/checkout.html"
    form_class = CheckoutForm

    def form_valid(self, form):
        cart = self.request.session.get("cart", {})
        if not cart:
            return redirect("shop:cart")
        order = Order.objects.create(
            full_name=form.cleaned_data["full_name"],
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            address=form.cleaned_data.get("address", ""),
        )
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, id=int(product_id), is_active=True)
            unit_price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                unit_price=unit_price,
                line_total=unit_price * qty,
            )
        order.recalculate_total()
        # Clear cart
        self.request.session["cart"] = {}
        return redirect("shop:success", order_id=order.id)


class CheckoutSuccessView(TemplateView):
    template_name = "shop/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_id"] = self.kwargs.get("order_id")
        return context


# Create your views here.
