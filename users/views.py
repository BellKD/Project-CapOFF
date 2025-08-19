from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            print("✅ Новый пользователь создан:", user.email)  # для проверки в консоли

            return redirect("index")  # должно отправить на главную
        else:
            print("❌ Ошибки формы:", form.errors)  # если что-то не так
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})
