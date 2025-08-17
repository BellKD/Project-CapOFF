from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from .models import Brand, Product, Category
from .serializers import BrandSerializer, ProductSerializer


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

    return render(request, "main/product_detail.html",
                  {"product": product,
                          "related_products": related_products
                   })


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
    return render(request, "main/catalog.html", {
        "products": products,
        "category_title": category_title
    })
