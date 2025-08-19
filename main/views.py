from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Brand, Product, Category, Basket, Subscriber
from .serializers import BrandSerializer, ProductSerializer, BasketSerializer


def index(request):
    brands = Brand.objects.filter(is_active=True)                   # HTML
    bestsellers = Product.objects.filter(is_active=True, category__title="Бестселлеры")
    sales = Product.objects.filter(is_active=True, category__title="Акции")

    return render(
        request,
        "main/index.html",
        {"brands": brands, "bestsellers": bestsellers, "sales": sales},
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
        brands = Brand.objects.filter(is_active=True)           #  API
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


class BasketAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = Product.objects.filter(pk=pk, is_active=True).first()
        if not product:
            return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(product, "stock") and product.stock < 1:
            return Response({"error": "Нет в наличии"}, status=status.HTTP_400_BAD_REQUEST)

        basket_item, created = Basket.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": 1}
        )
        if not created:
            basket_item.quantity = F("quantity") + 1
            basket_item.save()
            basket_item.refresh_from_db()

        return Response(BasketSerializer(basket_item).data, status=status.HTTP_201_CREATED)


@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    basket_item, created = Basket.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1}
    )
    if not created:
        basket_item.quantity = F("quantity") + 1
        basket_item.save()
        basket_item.refresh_from_db()

    return redirect("product_detail", pk=product.id)


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
