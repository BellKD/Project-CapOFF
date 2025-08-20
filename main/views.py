from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Brand, Product, Category, Basket, Subscriber, Storage, Favorite
from .serializers import BrandSerializer, ProductSerializer, BasketSerializer


def index(request):
    brands = Brand.objects.filter(is_active=True)  # HTML
    bestsellers = Product.objects.filter(is_active=True, category__title="Бестселлеры")
    sales = Product.objects.filter(is_active=True, category__title="Акции")

    # (товары за 1 день только для проверки)
    one_day_ago = timezone.now() - timedelta(days=1)
    new_products = Product.objects.filter(is_active=True, created_at__gte=one_day_ago)

    return render(
        request,
        "main/index.html",
        {
            "brands": brands,
            "bestsellers": bestsellers,
            "sales": sales,
            "new_products": new_products,
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    return render(
        request,
        "main/product_detail.html",
        {"product": product, "related_products": related_products}
    )


class HomePage(APIView):
    def get(self, request):
        brands = Brand.objects.filter(is_active=True)  # API
        bestsellers = Product.objects.filter(is_active=True, category__title="Бестселлеры")
        sales = Product.objects.filter(is_active=True, category__title="Акции")

        return Response({
            "brands": BrandSerializer(brands, many=True).data,
            "bestsellers": ProductSerializer(bestsellers, many=True).data,
            "sales": ProductSerializer(sales, many=True).data,
        })


class ProductDetail(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_active=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        return Response(ProductSerializer(product).data)


def catalog(request, category_title):
    products = Product.objects.filter(is_active=True, category__title=category_title)
    return render(
        request,
        "main/catalog.html",
        {"products": products, "category_title": category_title}
    )


@login_required
def basket_view(request):
    basket_items = Basket.objects.filter(user=request.user).select_related("product", "size")
    total_price = sum(item.product.price * item.quantity for item in basket_items)
    return render(
        request,
        "main/basket.html",
        {"basket_items": basket_items, "total_price": total_price}
    )


class BasketAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = Product.objects.filter(pk=pk, is_active=True).first()
        if not product:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        storage = Storage.objects.filter(product=product).first()
        if not storage or storage.quantity < 1:
            return Response({"error": "Нет в наличии"}, status=status.HTTP_400_BAD_REQUEST)

        basket_item, created = Basket.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": 1}
        )
        if not created:
            if storage.quantity < basket_item.quantity + 1:
                return Response({"error": "Недостаточно товара на складе"}, status=status.HTTP_400_BAD_REQUEST)
            basket_item.quantity = F("quantity") + 1
            basket_item.save()
            basket_item.refresh_from_db()

        return Response(BasketSerializer(basket_item).data, status=status.HTTP_201_CREATED)


class FavoriteAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = Product.objects.filter(pk=pk, is_active=True).first()
        if not product:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favorite.delete()
            return Response({"removed": "Товар удален из избранного"}, status=status.HTTP_200_OK)

        return Response({"added": "Товар добавлен в избранное"}, status=status.HTTP_201_CREATED)


class FavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related("product")
        products = [fav.product for fav in favorites]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    if request.method == "POST":
        size_id = request.POST.get("size")
        if not size_id:
            messages.error(request, "Выберите размер товара.")
            return redirect("product_detail", pk=product.id)

        storage = Storage.objects.filter(product=product, size_id=size_id).first()
        if not storage or storage.quantity < 1:
            messages.error(request, "Нет в наличии.")
            return redirect("product_detail", pk=product.id)

        basket_item, created = Basket.objects.get_or_create(
            user=request.user,
            product=product,
            size=storage.size,
            defaults={"quantity": 1}
        )

        if not created:
            if storage.quantity >= basket_item.quantity + 1:
                basket_item.quantity = F("quantity") + 1
                basket_item.save()
                basket_item.refresh_from_db()

        messages.success(request, f"{product.title} добавлен в корзину.")

    return redirect("product_detail", pk=product.id)


@login_required
def basket_update(request, item_id):
    item = get_object_or_404(Basket, id=item_id, user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "increase":
            if item.storage.quantity > item.quantity:
                item.quantity = F("quantity") + 1
                item.save()
        elif action == "decrease":
            if item.quantity > 1:
                item.quantity = F("quantity") - 1
                item.save()
    item.refresh_from_db()
    return redirect("basket")


@login_required
def basket_remove(request, item_id):
    item = get_object_or_404(Basket, id=item_id, user=request.user)
    if request.method == "POST":
        item.delete()
    return redirect("basket")


@login_required
def checkout(request):
    basket_items = Basket.objects.filter(user=request.user).select_related("product", "size")
    total_price = sum(item.product.price * item.quantity for item in basket_items)
    return render(request, "main/checkout.html", {"basket_items": basket_items, "total_price": total_price})


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"status": "error", "message": "Введите корректный email."})
            return render(request, "main/index.html", {"subscribe_message": "Введите корректный email."})

        if not Subscriber.objects.filter(email=email).exists():
            Subscriber.objects.create(email=email)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"status": "success", "message": "Подписка успешно оформлена!"})
            return render(request, "main/index.html", {"subscribe_message": "Подписка успешно оформлена!"})
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"status": "info", "message": "Вы уже подписаны."})
            return render(request, "main/index.html", {"subscribe_message": "Вы уже подписаны."})

    return JsonResponse({"status": "error", "message": "Неверный запрос"})


@login_required
def payment(request):
    basket_items = Basket.objects.filter(user=request.user).select_related("product", "size")
    total_price = sum(item.product.price * item.quantity for item in basket_items)
    return render(request, "main/payment.html", {"basket_items": basket_items, "total_price": total_price})


def search(request):
    query = request.GET.get("filter")

    products = Product.objects.filter(is_active=True)

    if query == "popular":
        products = products.filter(category__title="Бестселлеры")

    elif query == "new":
        last_30_days = timezone.now() - timedelta(days=30)
        products = products.filter(created_at__gte=last_30_days)

    return render(request, "main/search.html", {"products": products})


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("product")
    products = [fav.product for fav in favorites]
    return render(
        request,
        "main/saved.html",
        {"products": products, "page_title": "Сохранённые"},
    )


