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
    path("api/basket/add/<int:pk>/", views.BasketAddView.as_view(), name="basket_add"),
    path("basket/add/<int:product_id>/", views.add_to_basket, name="add_to_basket"),
    path("basket/", views.basket_view, name="basket"),
    path("basket/update/<int:item_id>/", views.basket_update, name="basket_update"),
    path("basket/remove/<int:item_id>/", views.basket_remove, name="basket_remove"),
    path("checkout/", views.checkout, name="checkout"),

    # Favorites
    path("api/favorite/add/<int:pk>/", views.FavoriteAddView.as_view(), name="favorite_add"),
    path("api/favorite/", views.FavoriteListView.as_view(), name="favorite_list"),
    path("saved/", views.favorites_view, name="saved"),


    # Checkout / Payment
    path("payment/", views.payment, name="payment"),

    # Search
    path("search/", views.search, name="search"),
]
