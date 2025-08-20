from django.urls import path
from .views import register, profile, delete_profile

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("profile/<str:section>/", profile, name="profile_section"),
    path("delete/", delete_profile, name="delete_profile"),
]
