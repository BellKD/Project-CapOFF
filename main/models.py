from django.db import models
from .constants import NULLABLE
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="brands/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="products/")
    description = models.TextField(**NULLABLE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="product_images/")


class Size(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Storage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class Banner(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="banners/")
    location = models.CharField(max_length=200, **NULLABLE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} -> {self.product.title}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
