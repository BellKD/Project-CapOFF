from django.urls import path
from . import views
from .views import index, product_detail, HomePage, ProductDetail, catalog

urlpatterns = [
    # HTML
    path("", index, name="index"),
    path("product/<int:pk>/", product_detail, name="product_detail"),

    # API
    path("api/home/", HomePage.as_view(), name="api_home"),
    path("api/product/<int:pk>/", ProductDetail.as_view(), name="api_product_detail"),

    # Catalogs
    path("bestsellers/", lambda r: catalog(r, "Бестселлеры"), name="bestsellers"),
    path("sales/", lambda r: catalog(r, "Акции"), name="sales"),
]
