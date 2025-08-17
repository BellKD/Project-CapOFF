from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Size, Storage, Banner


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price","discount_price","is_active")
    list_filter = ("is_active", "category")
    search_fields = ("title", "description")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "file")


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "size", "quantity")


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "location")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
