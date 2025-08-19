from django.urls import path
from . import views
from .views import index, product_detail, HomePage, ProductDetail, catalog

urlpatterns = [
    # HTML
    path("", index, name="index"),
    path("product/<int:pk>/", product_detail, name="product_detail"),
    path("subscribe/", views.subscribe, name="subscribe"),

    # API
    path("api/home/", HomePage.as_view(), name="api_home"),
    path("api/product/<int:pk>/", ProductDetail.as_view(), name="api_product_detail"),


    path("bestsellers/", lambda r: catalog(r, "Бестселлеры"), name="bestsellers"),
    path("sales/", lambda r: catalog(r, "Акции"), name="sales"),

    # Basket
    path("api/basket/add/<int:product_id>/", views.BasketAddView.as_view(), name="basket_add"),
    path("basket/add/<int:product_id>/", views.add_to_basket, name="add_to_basket"),
]
