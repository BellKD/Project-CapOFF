from rest_framework import serializers
from .models import Brand, Product, Basket, Favorite


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "title", "logo","is_active"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "cover", "price", "discount_price"]

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ["id", "product", "quantity"]

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "product","quantity", "created_at"]
