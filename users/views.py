from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from main.models import Product, Favorite  # импортируем для сохранённых


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Новый пользователь создан:", user.email)
            return redirect("index")
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request, section="orders"):
    saved_products = []
    if section == "saved":
        saved_products = Product.objects.filter(
            id__in=request.user.favorites.values_list("product_id", flat=True)
        )

    return render(request, "users/profile.html", {
        "user": request.user,
        "section": section,
        "saved_products": saved_products
    })



@login_required
def delete_profile(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("index")
    return redirect("profile")
